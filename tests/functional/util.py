from app.database import SessionFact, Base


def setup_db():
    """Create all database relations"""
    with SessionFact() as session:
        connection = session.connection()
        Base.metadata.create_all(connection)
        session.commit()


def teardown_db():
    """Remove all database relations"""
    with SessionFact() as session:
        connection = session.connection()
        Base.metadata.drop_all(connection)
        session.commit()
