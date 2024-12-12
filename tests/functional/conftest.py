import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.functional.util import setup_db, teardown_db


@pytest.fixture(scope="session")
def api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def reset_db():
    setup_db()
    yield
    teardown_db()
