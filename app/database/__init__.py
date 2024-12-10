from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, DEBUG

from .models import users


engine = create_engine(
    DATABASE_URL,
    isolation_level="READ COMMITTED",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=DEBUG,
)

SessionFact = sessionmaker(engine)
