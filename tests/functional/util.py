from sqlalchemy.orm import Session
from app.database import Base


def setup_db(sess: Session):
    """Create all database relations"""
    connection = sess.connection()
    Base.metadata.create_all(connection)
    sess.commit()


def teardown_db(sess: Session):
    """Remove all database relations"""
    connection = sess.connection()
    Base.metadata.drop_all(connection)
    sess.commit()
