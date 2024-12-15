import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionFact
from tests.functional.util import setup_db, teardown_db


@pytest.fixture(scope="session")
def api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def reset_db():
    with SessionFact() as sess:
        setup_db(sess=sess)
        sess.commit(sess=sess)
        yield
        teardown_db(sess=sess)
        sess.commit()
