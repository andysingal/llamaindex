# The builder image, used to build the virtual environment
FROM python:3.11-slim as builder

RUN apt-get update
RUN apt-get install build-essential -y

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# A directory to have app data 
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim as runtime

WORKDIR /app

COPY tests tests
COPY conf conf

RUN mkdir -p .streamlit
RUN touch .streamlit/secrets.toml

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY rag_assistant rag_assistant

CMD ["streamlit", "run", "rag_assistant/Hello.py", "--server.port", "80"]
