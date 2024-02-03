FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
    
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_IN_PROJECT true

RUN poetry install

EXPOSE ${PORT}

COPY app/ app/

CMD exec poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}