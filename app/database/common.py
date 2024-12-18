import time
from functools import wraps
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import DATABASE_URL, DEBUG

async_engine = create_async_engine(
    DATABASE_URL,
    isolation_level="READ COMMITTED",
    pool_pre_ping=False,  # True for pessimistic pre-ping before each checkout
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=DEBUG,
)

AsyncSessionMaker = async_sessionmaker(
    bind=async_engine,
    autobegin=True,  # session implicitly BEGINs a transation
    autoflush=True,  # all queries flush (database updates are sent to database)
    expire_on_commit=False,  # dont expire instances after commit
    twophase=False,  # no 2PC (in Postgres use isolation_level="SERIALIZABLE" instead)
)


def retry_on_deadlock(max_retries=3, wait_s: float = 0.1):
    """
    Decorator for retrying an aborted function due to a deadlock.

    Arguments:
        max_retries: How many times to retry the function
        wait_s: How long to wait between each retry (in seconds)

    The decorated function should not mutate args or kwargs and only contain one transaction,
    because the whole function will be retried with the same args and kwargs.
    Retry is triggered on `sqlalchemy.exc.OperationalError` if `"deadlock"` is in the error message.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except OperationalError as err:
                    if "deadlock" in str(err).lower():
                        retries += 1
                        if retries == max_retries:
                            raise err
                        time.sleep(wait_s)
                    else:
                        raise err

        return wrapper

    return decorator
