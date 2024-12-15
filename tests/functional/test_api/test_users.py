import pytest
from app.database import SessionFact
from httpx import AsyncClient
from tests.functional import util


@pytest.fixture(scope="module", autouse=True)
async def setup():
    async with SessionFact() as sess:
        await util.setup_db(sess=sess)
        await util.create_user(sess=sess, name="u1", fullname="user 1")
        await util.create_user(sess=sess, name="u2")
        await sess.commit()
        yield
        await util.teardown_db(sess=sess)
        await sess.commit()


class TestUsers:

    async def test_get_users(self, api_client: AsyncClient):
        resp = await api_client.get("/users")
        assert resp.status_code == 200
        data = resp.json()

        users: list[dict] = data["users"]
        assert len(users) == 2
        user_names = [d["name"] for d in users]

        user = users[user_names.index("u1")]
        assert user["fullname"] == "user 1"

        user = users[user_names.index("u2")]
        assert "fullname" not in user

    async def test_create_update_delete_user(self, api_client: AsyncClient):
        payload: dict = {"name": "u3", "fullname": "user 3"}
        resp = await api_client.post("/users", json=payload)
        assert resp.status_code == 201
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"
        pubid = user["pubid"]

        resp = await api_client.get(f"/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert user["fullname"] == "user 3"

        payload = {"fullname": None}
        resp = await api_client.put(f"/users/{pubid}", json=payload)
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = await api_client.get(f"/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = await api_client.delete(f"/users/{pubid}")
        assert resp.status_code == 200

        resp = await api_client.get(f"/users/{pubid}")
        assert resp.status_code == 404
