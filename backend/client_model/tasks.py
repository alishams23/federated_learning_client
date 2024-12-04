from celery import shared_task
from .models import ClientData, FederatedLearningResult
from client_model.flower_client_script import start_client


@shared_task
def start_federated_learning(client_data_id, file_path):
    try:
        # Retrieve the client data from the database
        client_data = ClientData.objects.get(id=client_data_id)

        # Run federated learning if not processed yet
        if client_data.status != 'processed':
            # Call the start_client function
            result = start_client(str(client_data.id), file_path)
            
            # Assume result is a dictionary containing federated metrics
            federated_metrics = result

            # Save federated learning results to the database
            # FederatedLearningResult.objects.create(
            #     # client=client_data,
            #     metrics=federated_metrics,
            #     model_path=f"models/{client_data.id}.pkl",
            # )

            # Update client data status
            # client_data.status = 'processed'
            # client_data.save()

            return {"status": "success", "metrics": federated_metrics}
        else:
            return {"status": "error", "message": "Client data already processed"}
    except ClientData.DoesNotExist:
        return {"status": "error", "message": "Client data not found"}
