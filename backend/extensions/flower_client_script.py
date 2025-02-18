import flwr as fl
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import joblib
import pickle
import requests



def load_csv_data(file_path: str):
    """
    Load client data from a CSV file. Assumes the last column is the target label.
    Args:
        file_path (str): Path to the CSV file.
    Returns:
        Tuple: (train_data, test_data) -> Each as (X, y)
    """
    # Load CSV file
    data = pd.read_csv(file_path)

    # Assume the last column is the target label
    X = data.iloc[:, :-1].values  # All columns except the last one as features
    y = data.iloc[:, -1].values   # The last column as the label

    # Preprocess labels for binary classification (if necessary)
    y = (y > 140).astype(int)  # Example: Convert to 0/1 binary classification

    # Normalize the feature data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return (X_train, y_train), (X_test, y_test)


def create_model():
    # Create a simple model for binary classification
    model = Sequential([
        Dense(16, activation='relu', input_shape=(10,)),  # Adjust input_shape based on feature count
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')  # Binary classification output
    ])
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model



def create_model():
    # Create a simple model for binary classification
    model = Sequential([
        Dense(16, activation='relu', input_shape=(10,)),  # Adjust input_shape based on feature count
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')  # Binary classification output
    ])
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


def save_final_model(model, data_id: str, format: str = 'h5') -> None:
    """
    Save the final model in TensorFlow's native formats (HDF5 or SavedModel).
    Args:
        model: Trained model to be saved.
        data_id (str): Unique identifier for the model.
        format (str): Format to save the model ('h5' or 'saved_model').
    """
    model_directory = "./media/model/"

    # Ensure the directory exists
    os.makedirs(model_directory, exist_ok=True)

    if format == 'h5':
        model_path = os.path.join(model_directory, f"{data_id}.h5")  # HDF5 format
        model.save(model_path)
    elif format == 'saved_model':
        model_path = os.path.join(model_directory, f"{data_id}_saved_model")  # SavedModel format
        model.save(model_path, save_format='tf')
    else:
        raise ValueError(f"Unsupported format '{format}'.")

    print(f"Model saved successfully: {model_path}")


def fetch_model_from_server(server_url: str):
    """
    Fetch the latest model weights from the main server.
    Args:
        server_url (str): The URL of the Django API to fetch the model.
    Returns:
        list: Model weights or None if no model exists on the server.
    """
    response = requests.get(f"{server_url}/api/model/get-model/")
    if response.status_code == 200:
        return pickle.loads(response.content)  # Deserialize model weights
    elif response.status_code == 404:
        print("No model found on the server. Using a new model.")
        return None  # Return None to indicate no model exists
    else:
        raise Exception("Failed to fetch model from server. Error code:", response.status_code)
    
    
class DiabetesClient(fl.client.NumPyClient):
    def __init__(self, model, train_data, test_data):
        self.model = model
        self.train_data = train_data
        self.test_data = test_data

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.train_data[0], self.train_data[1], epochs=1, batch_size=16)
        return self.model.get_weights(), len(self.train_data[0]), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.test_data[0], self.test_data[1])
        return loss, len(self.test_data[0]), {"accuracy": accuracy}


# def start_client(client_data_id: str, file_path: str):
#     """
#     Start the federated learning process for a client.
#     Args:
#         client_data_id (str): ID of the client.
#         file_path (str): Path to the CSV file.
#     Returns:
#         dict: Status and message for the client training.
#     """
#     # Load the data from the provided CSV file
#     train_data, test_data = load_csv_data(file_path)

#     # Initialize the model
#     model = create_model()

#     # Initialize and start the client
#     client = DiabetesClient(model, train_data, test_data)
#     fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)

#     # Save the final model
#     save_final_model(model, client_data_id)


def upload_model_to_server(server_url: str, model_weights):
    """
    Upload the model weights to the main server.
    Args:
        server_url (str): The URL of the Django API to upload the model.
        model_weights (list): Model weights to be uploaded.
    """
    serialized_weights = pickle.dumps(model_weights)
    response = requests.post(f"{server_url}/upload_model/", data=serialized_weights)
    if response.status_code == 200:
        print("Model uploaded successfully.")
    else:
        print("Failed to upload model to server. Error code:", response.status_code)




def start_client(client_data_id: str, file_path: str):
    """
    Start the federated learning process for a client.
    Args:
        client_data_id (str): ID of the client.
        file_path (str): Path to the CSV file.
    Returns:
        dict: Status, message, model location, and metrics for the client training.
    """
    # Load the data from the provided CSV file
    train_data, test_data = load_csv_data(file_path)

    # Initialize the model
    model = create_model()

    # Initialize and start the client
    client = DiabetesClient(model, train_data, test_data)
    
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)

    # Evaluate the final model
    loss, accuracy = model.evaluate(test_data[0], test_data[1], verbose=0)

    # Save the final model
    model_directory = "./media/model/"
    os.makedirs(model_directory, exist_ok=True)
    model_path = os.path.join(model_directory, f"{client_data_id}.joblib")
    save_final_model(model, client_data_id)

    # Return confirmation message, model location, and metrics
    return {
        "status": "success",
        "message": f"Federated learning complete for client {client_data_id}",
        "model_location": model_path,
        "metrics": {
            "loss": loss,
            "accuracy": accuracy
        }
    }


    # Return confirmation message
def start_client(client_data_id: str, file_path: str, server_url: str):
    """
    Start the federated learning process for a client.
    Args:
        client_data_id (str): ID of the client.
        file_path (str): Path to the CSV file.
        server_url (str): URL of the Django API server.
    Returns:
        list: Final model weights after training.
    """
    # Load the data from the provided CSV file
    train_data, test_data = load_csv_data(file_path)

    # Initialize the model
    model = create_model()

    # Fetch the global model weights from the main server
    global_weights = fetch_model_from_server(server_url)

    # If no model is found, initialize the model with random weights
    if global_weights:
        model.set_weights(global_weights)
    else:
        print("No model found on the server. Initializing with random weights.")

    # Initialize and start the client
    client = DiabetesClient(model, train_data, test_data)
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)


    
    
    loss, accuracy = model.evaluate(test_data[0], test_data[1], verbose=0)



    save_final_model(model, client_data_id)

    # Return confirmation message, model location, and metrics
    return {
        "status": "success",
        "message": f"Federated learning complete for client {client_data_id}",
        "model_location": model_path,
        "metrics": {
            "loss": loss,
            "accuracy": accuracy
        }
    }

    # Return the final model weights
    return model.get_weights()


# if __name__ == "__main__":
#     # Example usage: Replace 'client_data.csv' with your actual CSV file path
#     file_path = "client_data.csv"  # Path to CSV file
#     client_id = "client_1"  # Example client ID


#     # Start the client with provided data
#     result = start_client(client_id, file_path)
#     print(result)


# def start_client(client_data_id: str, file_path: str):
#     pass