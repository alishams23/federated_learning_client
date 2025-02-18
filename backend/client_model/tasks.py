from celery import shared_task
from .models import ClientData, FederatedLearningResult
import os
import requests
from django.conf import settings
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Replace with your broker URL
    backend='redis://localhost:6379/0'
)

@app.task(bind=True)
def start_federated_learning(self, client_data_id, file_path, executions=0):
    from extensions.flower_client_script import start_client

    try:
        # Check if we’ve already executed the task 5 times
        client_data = ClientData.objects.get(id=client_data_id)
        if executions >= client_data.repeat_count:
            return {"status": "completed", "message": "Task executed 5 times"}

        # Step 1: Retrieve the client data

        # Step 2: Run federated learning if not processed yet
        if client_data.status != 'processed':
            result = start_client(str(client_data.id), file_path,client_data.server.ip)  # Run federated learning
            federated_metrics = result["metrics"]

            # Step 3: Save federated learning results to the database
            FederatedLearningResult.objects.create(
                data=client_data,
                metrics=federated_metrics,
                model_path=result["model_location"],
            )

            # Step 4: Update client data status
            client_data.status = 'processed'
            client_data.save()

            # Step 5: Authenticate with the server using the login API
            login_url = f"{client_data.server.ip}/api/account/login/"
            create_url = f"{client_data.server.ip}/api/model/create/"

            login_payload = {
                "username": client_data.server.username,  # Username for login
                "password": client_data.server.password,  # Password for login
            }

            login_response = requests.post(login_url, data=login_payload)
            if login_response.status_code != 200:
                return {"status": "error", "message": "Failed to authenticate with the server"}

            token = login_response.json().get("token")

        # Prepare file for upload
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}

        with open(file_path, 'rb') as model_file:
            headers = {
                "Authorization": f"Token {token}",
            }
            files = {
                "model_path": model_file,
            }
            create_payload = {
                "lost": federated_metrics.get("loss"),
                "accuracy": federated_metrics.get("accuracy"),
            }
            create_response = requests.post(create_url, headers=headers, data=create_payload, files=files)

        if create_response.status_code != 201:
            return {
                "status": "error",
                "message": "Failed to create federated model",
                "details": create_response.json(),
            }

        # Schedule the next execution
        if executions < client_data.repeat_count - 1:  # Run 5 times total (0-4)
            from django.db.models import F
            client_data.repeated_count = F('repeated_count') + 1
            client_data.save()
            self.apply_async(
                args=[client_data_id, file_path, executions + 1],
                countdown=client_data.time_repeated  # Delay for 2 minutes
            )

        return {"status": "success", "message": f"Execution {executions + 1} completed successfully"}

    except ClientData.DoesNotExist:
        return {"status": "error", "message": "Client data not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
