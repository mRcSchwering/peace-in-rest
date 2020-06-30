# this python file uses the following encoding: utf-8
"""Sessions, Declarative Base

Session pool is instantiated with `get_db` helper for getting a session.
Include it as `Depends` in an endpoint definition to get a session object.
SQLAlchemy declarative base is instantiated.
"""
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import ResultProxy
from starlette.requests import Request
from app import settings, exceptions

connect_args = {}
if settings.SQLALCHEMY_DATABASE_URI.split(':')[0] == 'sqlite':
    connect_args['check_same_thread'] = False
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
                       connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.query = scoped_session(SessionLocal).query_property()


def get_db(request: Request) -> Session:
    return request.state.db
