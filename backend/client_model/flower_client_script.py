import flwr as fl
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
from typing import List, Tuple
import pickle
import logging

logging.basicConfig(level=logging.INFO)  # You can set the level to DEBUG, INFO, WARNING, etc.
logger = logging.getLogger(__name__)

# Function to save the model after training
def save_final_model(model, data_id: str, format: str = 'joblib') -> None:
    """ Save the final model to a specified path """
    logger.info(f'step 1')
    model_directory = "../media/model/"

    # Ensure the directory exists
    os.makedirs(model_directory, exist_ok=True)

    model_path = os.path.join(model_directory, f"{data_id}.{format}")  # Model file path

    # Save the model in the specified format
    if format == 'joblib':
        joblib.dump(model, model_path)
    elif format == 'pkl':
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    else:
        raise ValueError(f"Unsupported format '{format}'.")

    print(f"Model saved successfully: {model_path}")

class FlowerClient(fl.client.NumPyClient):
    def __init__(self, data: pd.DataFrame, data_id: str):
        self.data = data  # Client data
        self.data_id = data_id  # Client data ID
        self.model = LinearRegression()  # Model to train

    def get_parameters(self, config: dict = {}) -> List[np.ndarray]:
        logger.info(f'step 2')

        """Return model parameters as NumPy arrays."""
        # Ensure that the model is trained before accessing coef_ and intercept_
        if hasattr(self.model, 'coef_') and hasattr(self.model, 'intercept_'):
            logger.info(f'step 2 o1')
            return [self.model.coef_, np.array([self.model.intercept_])]
        else:
            # Return empty values if the model is not yet trained
            logger.info(f'step 2 o3')
            return [np.array([]), np.array([])]

    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        logger.info(f'step 3')
        """Set the model parameters (coefficients and intercept)."""
        if len(parameters[1]) > 0:
            self.model.coef_ = parameters[0]
            self.model.intercept_ = parameters[1][0]
        else:
            # Handle the case where parameters[1] is empty (e.g., do nothing)
            # You can log a message or perform an alternative action if needed
            logger.info("Received empty intercept parameters.")

    def fit(self, parameters: List[np.ndarray], config: dict = None) -> Tuple[List[np.ndarray], int, dict[str, float]]:
        logger.info(f'step 4')
        """Train the model using local data."""
        self.set_parameters(parameters)

        # Prepare data (X: features, y: target)
        X = self.data[['Area', 'Room', 'Parking', 'Warehouse', 'Elevator']].values
        y = self.data['Price'].values

        # Fit the model
        self.model.fit(X, y)

        # Calculate and return the loss (Mean Squared Error)
        predictions = self.model.predict(X)
        mse = np.mean((predictions - y) ** 2)

        # Save the final model after training
        save_final_model(self.model, self.data_id, format="joblib")

        # Get the number of data points used for training
        num_data_points = len(self.data)

        # Return the updated parameters, number of data points, and MSE
        return self.get_parameters(), num_data_points, {"mse": float(mse)}


# Client-side function to start the federated learning process
def start_client(client_data_id: str, file_path: str) -> dict:
    """Start the federated learning process for a client."""
    # Load the client data (assuming CSV file for now)
    client_data = pd.read_csv(file_path)  # Adjust this to load your specific data

    # Initialize the FlowerClient with the loaded data
    client = FlowerClient(client_data, str(client_data_id))

    # Start the federated learning process by using Flower's client API
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)

    # Return a dictionary containing federated metrics (e.g., MSE)
    return {
        "status": "success",
        "message": "Federated learning complete",
    }