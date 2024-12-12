import pytest
from fastapi.testclient import TestClient
from app.database import SessionFact
from app.services import user_service
from tests.functional.util import setup_db, teardown_db


class TestUsers:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        setup_db()
        with SessionFact() as sess:
            user_service.create_user(sess=sess, name="u1", fullname="user 1")
            user_service.create_user(sess=sess, name="u2")
        yield
        teardown_db()

    def test_get_users(self, api_client: TestClient):
        resp = api_client.get("/v1/users")
        assert resp.status_code == 200
        data = resp.json()

        users: list[dict] = data["users"]
        assert len(users) == 2
        user_names = [d["name"] for d in users]

        user = users[user_names.index("u1")]
        assert user["fullname"] == "user 1"

        user = users[user_names.index("u2")]
        assert "fullname" not in user

    def test_create_update_delete_user(self, api_client: TestClient):
        payload: dict = {"name": "u3", "fullname": "user 3"}
        resp = api_client.post("/v1/users", json=payload)
        assert resp.status_code == 201
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"
        pubid = user["pubid"]

        resp = api_client.get(f"/v1/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"

        payload = {"fullname": None}
        resp = api_client.put(f"/v1/users/{pubid}", json=payload)
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = api_client.get(f"/v1/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = api_client.delete(f"/v1/users/{pubid}")
        assert resp.status_code == 200

        resp = api_client.get(f"/v1/users/{pubid}")
        assert resp.status_code == 404
