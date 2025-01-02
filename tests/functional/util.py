from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from app.database.models import user_models, item_models
from app.modules.auth import hash_password, create_access_token


async def setup_db(sess: AsyncSession):
    """Create all database relations"""
    conn = await sess.connection()
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)
    await sess.commit()


async def teardown_db(sess: AsyncSession):
    """Remove all database relations"""
    conn = await sess.connection()
    await conn.run_sync(Base.metadata.drop_all)
    await sess.commit()


async def create_user(
    sess: AsyncSession,
    name: str,
    password: str = "MyPass1234!",
    fullname: str | None = None,
) -> user_models.User:
    """Create a user"""
    params = {
        "name": name,
        "fullname": fullname,
        "password_hash": hash_password(password),
    }
    stmt = insert(user_models.User).returning(user_models.User)
    res = await sess.execute(stmt, params)
    return res.scalars().one()


def create_user_access_token(name: str) -> str:
    """Generate access token for a user"""
    return create_access_token(sub=name)


async def create_item(
    sess: AsyncSession, user_pubid: str, name: str
) -> item_models.Item:
    """Create an item for a user"""
    params = {"name": name, "user_id": user_pubid}
    stmt = insert(item_models.Item).returning(item_models.Item)
    res = await sess.execute(stmt, params)
    return res.scalars().one()
