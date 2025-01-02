import pytest
from app.database import AsyncSessionMaker
from httpx import AsyncClient
from tests.functional import util


@pytest.fixture(scope="module", autouse=True)
async def setup():
    async with AsyncSessionMaker() as sess:
        await util.setup_db(sess=sess)
        user = await util.create_user(sess=sess, name="u1", fullname="user 1")
        await util.create_item(sess=sess, user_pubid=user.id, name="u1i1")
        await util.create_item(sess=sess, user_pubid=user.id, name="u1i2")
        await util.create_user(sess=sess, name="u2")
        await sess.commit()
        u1_token = util.create_user_access_token(name="u1")
        yield {"u1_id": user.id, "u1_token": u1_token}
        await util.teardown_db(sess=sess)
        await sess.commit()


class TestUsers:
    u1_id: str
    auth_headers: dict

    @pytest.fixture(scope="function", autouse=True)
    async def setup(self, setup: dict):
        self.u1_id = setup["u1_id"]
        self.auth_headers = {"Authorization": f"Bearer {setup['u1_token']}"}

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

        params = {"incl_items": True}
        resp = await api_client.get(f"/users/{self.u1_id}", params=params)
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u1"
        items = user["items"]
        assert items[0]["name"] == "u1i1"
        assert items[1]["name"] == "u1i2"

    async def test_delete_user_with_items(self, api_client: AsyncClient):
        resp = await api_client.delete(
            f"/users/{self.u1_id}", headers=self.auth_headers
        )
        assert resp.status_code == 200

        resp = await api_client.get(f"/users/{self.u1_id}")
        assert resp.status_code == 404

        params = {"user_pubid": self.u1_id}
        resp = await api_client.get("/items", params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 0

    async def test_create_update_delete_user(self, api_client: AsyncClient):
        payload: dict = {"name": "u3", "fullname": "user 3", "password": "MyPass1234!"}
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
        resp = await api_client.put(
            f"/users/{pubid}", json=payload, headers=self.auth_headers
        )
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = await api_client.get(f"/users/{pubid}")
        assert resp.status_code == 200
        user = resp.json()

        assert user["name"] == "u3"
        assert "fullname" not in user

        resp = await api_client.delete(f"/users/{pubid}", headers=self.auth_headers)
        assert resp.status_code == 200

        resp = await api_client.get(f"/users/{pubid}")
        assert resp.status_code == 404
