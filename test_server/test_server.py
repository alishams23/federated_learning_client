import flwr as fl

strategy = fl.server.strategy.FedAvg()
config = fl.server.ServerConfig(num_rounds=3)

print("Starting server...")
fl.server.start_server(
    server_address="127.0.0.1:8080",
    strategy=strategy,
    config=config
)