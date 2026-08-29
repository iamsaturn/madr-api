FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

COPY madr_api ./madr_api
COPY migrations ./migrations
COPY alembic.ini ./
COPY entrypoint.sh ./

CMD ["sh", "./entrypoint.sh"]