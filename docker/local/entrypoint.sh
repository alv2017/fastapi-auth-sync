#!/bin/bash
set -e

echo "Waiting for Postgres..."
sleep 5 # Simple wait, replace with a proper wait-for-it script in production

echo "Postgres ready, running migrations..."
uv run alembic upgrade head

echo "Starting FastAPI..."
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000