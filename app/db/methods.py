# this python file uses the following encoding: utf-8
from sqlalchemy.orm import Session
from app.db import fetchall, fetchone


def greet(name: str) -> str:
    return 'hi ' + name
