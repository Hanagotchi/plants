FROM python:3.11-slim-buster

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_IN_PROJECT true

RUN poetry install

EXPOSE ${PORT}

ADD app/ ./app/

CMD exec poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}