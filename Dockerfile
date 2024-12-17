# base image
FROM python:3.11 AS base
COPY ./app /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# tests image
FROM base AS tests
COPY ./tests /tests
COPY ./pytest.ini /pytest.ini
RUN pip install --no-cache-dir --upgrade -r /tests/requirements.txt
CMD ["pytest", "tests"]

# migrations image
FROM base AS migrations
COPY ./migrations /migrations
COPY ./alembic.ini /alembic.ini
RUN pip install --no-cache-dir --upgrade -r /migrations/requirements.txt
CMD ["alembic","upgrade","head"]

# app image
FROM base AS app
EXPOSE 80
CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
