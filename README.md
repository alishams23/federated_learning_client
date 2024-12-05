# Federated learning client

## Introduction

This project utilizes Docker Compose to orchestrate multiple services required for the application. The services included are:

- **backend**: The main application backend, built from the `DockerFile` located in the `./backend` directory.
- **redis**: A Redis instance pulled from `docker.arvancloud.ir/redis:latest`.
- **test_server**: A test server, built from the `DockerFile` in the `./test_server` directory.

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. [Download Docker](https://www.docker.com/get-started).
- **Docker Compose**: Comes bundled with Docker Desktop. Verify installation by running:

  ```bash
  docker-compose --version
  ```

## Setup and Usage

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/alishams23/federated_learning_client.git
cd federated_learning_client
```

### 2. Build and Run the Services

Build the images and start the services using Docker Compose:

```bash
docker-compose up --build
```

This command will:

- Build Docker images for `backend` and `test_server`.
- Pull the Redis image from `docker.arvancloud.ir/redis:latest`.
- Start all services defined in the `docker-compose.yml`.
    
### 3. Access the Services

- **backend**: [http://localhost:8000](http://localhost:8000)
- **redis**: Accessible on port `6379` (for internal service communication).
- **test_server**: [http://localhost:8080](http://localhost:8080)

### 4. Run Services in the Background

To run the services in detached mode:

```bash
docker-compose up --build -d
```

### 5. Stop the Services

Gracefully stop and remove the containers:

```bash
docker-compose down
```

## Additional Commands

### View Service Logs

To view logs from all services:

```bash
docker-compose logs -f
```

To view logs from a specific service:

```bash
docker-compose logs -f <service-name>
```

Replace `<service-name>` with `backend`, `redis`, or `test_server`.

### Rebuild a Specific Service

If you've made changes and need to rebuild a service:

```bash
docker-compose build <service-name>
docker-compose up -d <service-name>
```

### Scale Services

To scale the `backend` service (e.g., run 3 instances):

```bash
docker-compose up -d --scale backend=3
```

## Notes

- Ensure that the `DockerFile` in both `./backend` and `./test_server` directories are correctly set up.
- If you encounter issues pulling the Redis image, verify access permissions to `docker.arvancloud.ir`.

## Troubleshooting

- **Port Conflicts**: If ports `8000`, `8080`, or `6379` are in use, modify the `ports` section in `docker-compose.yml`.
- **Permission Errors**: Some commands may require `sudo` privileges.

---