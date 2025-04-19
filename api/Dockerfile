FROM python:3.12-slim

RUN apt update \
    && apt install \
        --no-install-recommends \
        -y \
        curl

WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction
COPY ./src ./src

ENV FASTAPI_APP_KEYCLOAK_URL=${FASTAPI_APP_KEYCLOAK_URL}
ENV FASTAPI_APP_KEYCLOAK_REALM=${FASTAPI_APP_KEYCLOAK_REALM}

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
