# this python file uses the following encoding: utf-8
from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
