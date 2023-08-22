FROM python:3.11-alpine

ENV PYTHONBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN pip install --upgrade pip

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml entrypoint.sh ./

RUN poetry install --no-interaction --no-ansi --no-dev --no-root

COPY ./core core
COPY ./apps apps
COPY ./manage.py manage.py
COPY ./tests tests

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
