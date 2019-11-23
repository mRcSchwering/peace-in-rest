# this python file uses the following encoding: utf-8
"""Testing Utils

Imports models and session factory from app.db to initialize a database session
and provide a `reset_testdata()` function.
Also, testing helper function `get()`.
Assumes that app is running on http://localhost:8000.
Overwrite with ENV HOST. This is used in docker-compose testing workflow.
"""
import requests
import os
from app.db import models, SessionLocal, engine


db = SessionLocal()
host = os.environ.get('HOST', 'http://localhost:8000')


def get(uri, timeout=1):
    return requests.get(host + uri, timeout=timeout)


def reset_testdata():
    print('resetting testdata')
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db.add_all([
        models.User(email='user1@email', hashed_password='pass1'),
        models.User(email='user2@email', hashed_password='pass2'),
        models.User(email='user3@email', hashed_password='pass3')
    ])
    db.commit()


if __name__ == '__main__':
    reset_testdata()
