import time
import datetime as dt


def utcnow() -> dt.datetime:
    """Get naive datetime of the current UTC time (not host's timezone)"""
    return dt.datetime.now() + dt.timedelta(seconds=time.timezone)
