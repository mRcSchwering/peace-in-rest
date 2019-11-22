import requests
from app import models
from app.db import SessionLocal, engine

db = SessionLocal()
host = 'http://localhost:8000'


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
    reset_testdata(db)
