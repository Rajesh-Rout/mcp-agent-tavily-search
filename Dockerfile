FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (better caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the project
COPY . .

CMD ["uv", "run", "agent.py"]