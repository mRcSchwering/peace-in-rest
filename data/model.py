# this python file uses the following encoding: utf-8
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# central engine and Base
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


# define model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.name, self.password)


# create tables
Base.metadata.create_all(engine)


# work with session
Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    User(name='u1', password='u1'),
    User(name='u2', password='u2')
])

session.commit()


# views
class UserViews(object):

    def __init__(self, session):
        self.session = session

    def is_login_valid(self, user, password):
        for u, p in self.session.query(User.name, User.password):
            if user == u:
                if password == p:
                    return True
        return False


userViews = UserViews(session)

userViews.is_login_valid('u1', 'u1')
