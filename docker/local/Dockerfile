FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Copy dependencies first
COPY pyproject.toml uv.lock .env.docker /app/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --dev --no-install-project

# Copy project files
COPY . /app/
COPY docker/local/entrypoint.sh /app/entrypoint.sh
RUN mv .env.docker .env
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
