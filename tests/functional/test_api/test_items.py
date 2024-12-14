import pytest
from fastapi.testclient import TestClient
from app.database import SessionFact
from app.services import user_service, item_service
from tests.functional.util import setup_db, teardown_db


@pytest.fixture(scope="module", autouse=True)
def setup():
    setup_db()
    with SessionFact() as sess:
        user1 = user_service.create_user(sess=sess, name="u1")
        item_service.create_item(sess=sess, user_pubid=user1.id, name="i1")
        item_service.create_item(sess=sess, user_pubid=user1.id, name="i2")
        user_service.create_user(sess=sess, name="u2")
        sess.commit()
    yield {"u1_id": user1.id}
    teardown_db()


class TestItems:
    u1_id: str

    @pytest.fixture(autouse=True)
    def setup(self, setup: dict):
        self.u1_id = setup["u1_id"]

    def test_get_items(self, api_client: TestClient):
        params = {"user_pubid": self.u1_id}
        resp = api_client.get("/items", params=params)
        assert resp.status_code == 200
        data = resp.json()

        items: list[dict] = data["items"]
        assert len(items) == 2
        item_names = [d["name"] for d in items]

        item = items[item_names.index("i1")]
        print(item)
        assert item["fullname"] == "user 1"

        item = items[item_names.index("i2")]
        assert "fullname" not in item

    def test_create_update_delete_user(self, api_client: TestClient):
        payload: dict = {"name": "u3", "fullname": "user 3"}
        resp = api_client.post("/users", json=payload)
        assert resp.status_code == 201
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"
        pubid = user["pubid"]

        resp = api_client.get(f"/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"

        payload = {"fullname": None}
        resp = api_client.put(f"/users/{pubid}", json=payload)
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = api_client.get(f"/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = api_client.delete(f"/users/{pubid}")
        assert resp.status_code == 200

        resp = api_client.get(f"/users/{pubid}")
        assert resp.status_code == 404
