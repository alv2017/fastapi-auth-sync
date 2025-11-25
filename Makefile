.PHONY: help
help:  ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint:  ## Linter the code.
	@echo "Linting Code"
	uv run ruff check api tests --fix --show-fixes


.PHONY: format
format:  ## Format the code.
	@echo "Code Formatting"
	uv run ruff format


.PHONY: test
test:  ## Test your code locally
	@echo "--> Copying .env.test to .env"
	cp .env.test .env

	@echo "--> Starting docker container with test database"
	docker compose -f docker/db-test/docker-compose.yml up --build -d

	@echo "--> Running tests"
	uv run pytest tests/ -svv --cov=api --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under 80

	@echo "--> Stopping docker container with test database"
	docker compose -f docker/db-test/docker-compose.yml down

	@echo "--> Restoring .env file"
	rm .env


.PHONY: run-dev
run-dev:  ## Run application locally with development database
	@echo "--> Copying .env.dev to .env"
	cp .env.dev .env

	@echo "--> Starting docker container with development database"
	docker compose -f docker/db/docker-compose.yml up --build -d

	@echo "--> Waiting for database to be ready"
	sleep 5

	@echo "--> Applying database migrations"
	uv run alembic upgrade head

	@echo "--> Running application"
	uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload


.PHONY: stop-dev
stop-dev:  ##
	@echo "--> Stopping Uvicorn server"
	- pkill -f "uvicorn api.main:app" || true

	@echo "--> Stopping development database container"
	docker compose -f docker/db/docker-compose.yml down

	@echo "--> Cleaning up .env"
	- rm .env || true

	@echo "--> Development environment stopped"


.PHONY: start-db
start-db:  ##
	@echo "--> Starting PostgreSQL database container"
	docker compose -f docker/db/docker-compose.yml up --build -d

	@echo "--> Waiting for database to be ready"
	sleep 5

	@echo "--> Applying database migrations"
	uv run alembic upgrade head


.PHONY: stop-db
stop-db:  ##
	@echo "--> Stopping PostgreSQL database container"
	docker compose -f docker/db/docker-compose.yml down
