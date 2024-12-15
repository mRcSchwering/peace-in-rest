import os
import logging


DEBUG = bool(os.environ.get("DEBUG", 0))
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://admin:admin@0.0.0.0:5432/main"
)

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
