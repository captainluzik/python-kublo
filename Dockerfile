FROM python:3.11

ENV PYTHONBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml docker-entrypoint.sh ./

RUN poetry install --no-interaction --no-ansi --only main --no-root

COPY . .

EXPOSE 8000
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
