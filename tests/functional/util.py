from app.database import SessionFact, Base


def setup_db():
    with SessionFact() as session:
        connection = session.connection()
        Base.metadata.create_all(connection)
        session.commit()


def teardown_db():
    with SessionFact() as session:
        connection = session.connection()
        Base.metadata.drop_all(connection)
        session.commit()
