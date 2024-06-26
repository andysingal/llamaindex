FROM python:3.11

WORKDIR /app

# Poetry Settings
## Set Poetry to non-interactive mode to avoid user interaction during builds
ENV POETRY_NO_INTERACTION=1
## Specify a cache directory for Poetry to improve build speeds and manage cache effectively
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
## Disable Python's buffering to ensure that logs are streamed to the console immediately
ENV PYTHONUNBUFFERED 1
## Prevent Python from writing bytecode files (.pyc) to reduce image size
ENV PYTHONDONTWRITEBYTECODE 1


# Install Poetry
## Disable the creation of virtual environments to keep the setup light
RUN pip install --no-cache-dir poetry==1.4.2 && poetry config virtualenvs.create false

# Copy dependency files
## Only copy the pyproject.toml and poetry.lock files initially to leverage Docker cache
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Install dependencies
## If dependency files have not changed, this layer will be cached by Docker
RUN poetry install --no-root --no-interaction --no-ansi