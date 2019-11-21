# this python file uses the following encoding: utf-8
import logging
import app.settings as settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import ResultProxy
from starlette.requests import Request
from app.exceptions import NoResultFound
from typing import List, Dict

log = logging.getLogger(__name__)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(request: Request) -> Session:
    return request.state.db


def fetchall(query: ResultProxy) -> List[dict]:
    rows = query.fetchall()
    return [dict(d) for d in rows]


def fetchone(query: ResultProxy) -> dict:
    row = query.fetchone()
    if row is None:
        raise NoResultFound('No results found')
    return dict(row)
