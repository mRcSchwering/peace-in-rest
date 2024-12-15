import pytest
import datetime as dt
from fastapi.testclient import TestClient
from app.database import SessionFact
from app.services import user_service, item_service
from tests.functional.util import setup_db, teardown_db


@pytest.fixture(scope="module", autouse=True)
def setup():
    with SessionFact() as sess:
        setup_db(sess=sess)
        user1 = user_service.create_user(sess=sess, name="u1")
        item_service.create_item(sess=sess, user_pubid=user1.id, name="u1i1")
        item_service.create_item(sess=sess, user_pubid=user1.id, name="u1i2")
        user2 = user_service.create_user(sess=sess, name="u2")
        item_service.create_item(sess=sess, user_pubid=user2.id, name="u2i1")
        sess.commit()
        yield {"u1_id": user1.id, "u2_id": user2.id}
        teardown_db(sess=sess)
        sess.commit()


class TestItems:
    u1_id: str
    u2_id: str

    @pytest.fixture(autouse=True)
    def setup(self, setup: dict):
        self.u1_id = setup["u1_id"]
        self.u2_id = setup["u2_id"]

    def test_get_items(self, api_client: TestClient):
        params = {"user_pubid": self.u1_id}
        resp = api_client.get("/items", params=params)
        assert resp.status_code == 200
        data = resp.json()

        items: list[dict] = data["items"]
        assert len(items) == 2

        for item in items:
            assert dt.datetime.fromisoformat(item["added"])

        params = {"user_pubid": self.u2_id}
        resp = api_client.get("/items", params=params)
        assert resp.status_code == 200
        data = resp.json()

        items = data["items"]
        assert len(items) == 1

        for item in items:
            assert item["user_pubid"] == self.u2_id
            assert dt.datetime.fromisoformat(item["added"])

    def test_create_update_delete_item(self, api_client: TestClient):
        payload: dict = {"name": "u1i3", "user_pubid": self.u1_id}
        resp = api_client.post("/items", json=payload)
        assert resp.status_code == 201
        item = resp.json()

        assert item["name"] == "u1i3"
        assert item["user_pubid"] == self.u1_id
        assert dt.datetime.fromisoformat(item["added"])
        pubid = item["pubid"]

        resp = api_client.get(f"/items/{pubid}")
        assert resp.status_code == 200
        item = resp.json()

        assert item["name"] == "u1i3"
        assert item["user_pubid"] == self.u1_id
        assert dt.datetime.fromisoformat(item["added"])
        pubid = item["pubid"]

        payload = {"added": "2024-12-12 13:25"}
        resp = api_client.put(f"/items/{pubid}", json=payload)
        assert resp.status_code == 200
        item = resp.json()

        assert item["name"] == "u1i3"
        assert item["user_pubid"] == self.u1_id
        assert item["added"] == "2024-12-12T13:25:00"

        resp = api_client.get(f"/items/{pubid}")
        assert resp.status_code == 200
        item = resp.json()

        assert item["name"] == "u1i3"
        assert item["user_pubid"] == self.u1_id
        assert item["added"] == "2024-12-12T13:25:00"

        resp = api_client.delete(f"/items/{pubid}")
        assert resp.status_code == 200

        resp = api_client.get(f"/items/{pubid}")
        assert resp.status_code == 404
