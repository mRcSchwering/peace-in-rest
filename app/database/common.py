from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, DEBUG

engine = create_engine(
    DATABASE_URL,
    isolation_level="READ COMMITTED",
    pool_pre_ping=False,  # True for pessimistic pre-ping before each checkout
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=DEBUG,
)

SessionFact = sessionmaker(
    bind=engine,
    autobegin=True,  # session implicitly BEGINs a transation
    autoflush=True,  # all queries flush (database updates are sent to database)
    expire_on_commit=False,  # dont expire instances after commit
    twophase=False,  # no 2PC (in Postgres use isolation_level="SERIALIZABLE" instead)
)
