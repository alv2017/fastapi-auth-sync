# Fastapi-Auth-Sync

FastAPI application with a synchronous hashing function used for authentication.

## 1. Running the Application Locally

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

# 2. Running the Application Locally with Docker

```bash
docker compose -f docker/local/docker-compose.yml up --build
```

or you can first build the image and then run the container:

```bash
docker compose -f docker/local/docker-compose.yml build
docker compose -f docker/local/docker-compose.yml up
```

Stopping the application:

```bash
docker compose -f docker/local/docker-compose.yml down
```
