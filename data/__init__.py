# this python file uses the following encoding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base
from .models import models
from .connector import Connector

# initializing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# public interface
conn = Connector(session)
