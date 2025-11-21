# Fastapi-Auth-Sync

FastAPI application with a synchronous hashing function used for authentication.

## 1. Running the Application Locally

start the development database server and run the application

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

## 2. Running the Application Locally with Docker

Location of the docker-compose file: `docker/local/docker-compose.yml`

```bash
docker compose -f docker/local/docker-compose.yml up --build
```

or you can first build the image and then run the container:

```bash
docker compose -f docker/local/docker-compose.yml build
docker compose -f docker/local/docker-compose.yml up
```

stopping the application:

```bash
docker compose -f docker/local/docker-compose.yml down
```

## 3. Running Databases Locally using Docker

### 3.1 Development Database

Location of the docker-compose file: `docker/db/docker-compose.yml`

start the development database server:

```bash
docker compose -f docker/db/docker-compose.yml up --build
```

or you can first build the image and then run the container:

```bash
docker compose -f docker/db/docker-compose.yml build
docker compose -f docker/db/docker-compose.yml up
```

stop the development database server:

```bash
docker compose -f docker/db/docker-compose.yml down
```

### 3.2 Test Database

Location of the docker-compose file: `docker/db-test/docker-compose.yml`

start the test database server:

```bash
docker compose -f docker/db-test/docker-compose.yml up --build
```

or you can first build the image and then run the container:

```bash
docker compose -f docker/db-test/docker-compose.yml build
docker compose -f docker/db-test/docker-compose.yml up
```

stop the test database server:

```bash
docker compose -f docker/db-test/docker-compose.yml down
```