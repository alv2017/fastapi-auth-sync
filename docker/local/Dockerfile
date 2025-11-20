FROM ghcr.io/astral-sh/uv:python3.13-bookworm


WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY ./pyproject.toml /app/pyproject.toml

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project && pip install uvicorn

# Copy project directories
COPY ./api /app/api
COPY ./alembic /app/alembic
COPY ./tests /app/tests
COPY ./logs /app/logs

# Copy project files
COPY ./alembic.ini README.md /app/
COPY ./README.md /app/
COPY ./.env.docker /app/.env

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
