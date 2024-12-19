import os
import logging


DEBUG = bool(os.environ.get("DEBUG", 0))
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://admin:admin@0.0.0.0:5432/main"
)

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# TODO: better naming?

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
