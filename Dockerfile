FROM python:3.10-slim as builder

RUN pip install --no-cache-dir poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

FROM python:3.10-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
	PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY ./init_db.py ./init_db.py
COPY api/* ./api
COPY tests/* ./tests
COPY ./start.sh ./start.sh

RUN chmod +x start.sh && chmod +x init_db.py

EXPOSE 5000
CMD ["bash", "start.sh"]
