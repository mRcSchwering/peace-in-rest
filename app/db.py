# this python file uses the following encoding: utf-8
import logging
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import ResultProxy
from starlette.requests import Request
from app import settings, exceptions

log = logging.getLogger(__name__)

connect_args = {}
if settings.SQLALCHEMY_DATABASE_URI.split(':')[0] == 'sqlite':
    connect_args['check_same_thread'] = False
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(request: Request) -> Session:
    return request.state.db


def fetchall(query: ResultProxy) -> List[dict]:
    rows = query.fetchall()
    return [dict(d) for d in rows]


def fetchone(query: ResultProxy) -> dict:
    row = query.fetchone()
    if row is None:
        raise exceptions.NoResultFound('No results found')
    return dict(row)
