import pytest
from fastapi import HTTPException
from app.database import AsyncSessionMaker
from app.services import auth_service
from tests.functional import util


@pytest.fixture(scope="module", autouse=True)
async def setup():
    async with AsyncSessionMaker() as sess:
        await util.setup_db(sess=sess)
        user1 = await util.create_user(sess=sess, name="u1", password="U1Pass1234!")
        await sess.commit()
        yield {"u1_id": user1.id}
        await util.teardown_db(sess=sess)
        await sess.commit()


class TestService:
    u1_id: str

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, setup: dict):
        self.u1_id = setup["u1_id"]

    async def test_generate_and_parse_valid_user_tokens(self):
        tokens = auth_service.generate_user_tokens(user_pubid=self.u1_id)

        for token in tokens:
            async with AsyncSessionMaker() as sess:
                user = await auth_service.parse_token_and_get_user(
                    sess=sess, token=token
                )

            assert user.name == "u1"

    async def test_generate_and_parse_nonexistent_user_tokens(self):
        tokens = auth_service.generate_user_tokens(user_pubid="asd")

        for token in tokens:
            async with AsyncSessionMaker() as sess:
                with pytest.raises(HTTPException):
                    await auth_service.parse_token_and_get_user(sess=sess, token=token)

    async def test_check_valid_login_credentials(self):
        async with AsyncSessionMaker() as sess:
            user = await auth_service.check_login_credentials_and_get_user(
                sess=sess, username="u1", password="U1Pass1234!"
            )

        assert user.name == "u1"
