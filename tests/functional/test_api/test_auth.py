import pytest
from httpx import AsyncClient
from app.database import AsyncSessionMaker
from tests.functional import util


@pytest.fixture(scope="module", autouse=True)
async def setup():
    async with AsyncSessionMaker() as sess:
        await util.setup_db(sess=sess)
        user1 = await util.create_user(sess=sess, name="u1", password="U1Pass1234!")
        user2 = await util.create_user(sess=sess, name="u2", password="U2Pass1234!")
        await sess.commit()
        yield {"u1_id": user1.id, "u2_id": user2.id}
        await util.teardown_db(sess=sess)
        await sess.commit()


class TestAccessTokens:
    u1_id: str
    u2_id: str

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, setup: dict):
        self.u1_id = setup["u1_id"]
        self.u2_id = setup["u2_id"]

    async def test_get_and_refresh_access_token(self, api_client: AsyncClient):
        payload = {"username": "u1", "password": "U1Pass1234!"}
        resp = await api_client.post("/auth/token", data=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert len(data["access_token"]) > 0
        assert len(data["refresh_token"]) > 0
        assert data["token_type"] == "bearer"

        payload = {"refresh_token": data["refresh_token"]}
        resp = await api_client.post("/auth/refresh", data=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert len(data["access_token"]) > 0
        assert len(data["refresh_token"]) > 0
        assert data["token_type"] == "bearer"

    async def test_deny_access_token(self, api_client: AsyncClient):
        data = {"username": "u1"}
        resp = await api_client.post("/auth/token", data=data)
        assert resp.status_code == 422

        data = {"username": "u1", "password": "WrongPass1234!"}
        resp = await api_client.post("/auth/token", data=data)
        assert resp.status_code == 401

        data = {"username": "u2", "password": "U1Pass1234!"}
        resp = await api_client.post("/auth/token", data=data)
        assert resp.status_code == 401

        data = {"username": "u3", "password": "U1Pass1234!"}
        resp = await api_client.post("/auth/token", data=data)
        assert resp.status_code == 401

    async def test_deny_refresh_token(self, api_client: AsyncClient):
        data = {"refresh_token": "asd"}
        resp = await api_client.post("/auth/refresh", data=data)
        assert resp.status_code == 401
