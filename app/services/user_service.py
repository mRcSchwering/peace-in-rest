from typing import Sequence
import logging
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import user_models

log = logging.getLogger(__name__)


async def get_all_users(sess: AsyncSession) -> Sequence[user_models.User]:
    stmt = select(user_models.User)
    res = await sess.scalars(stmt)
    return res.all()


async def get_user_by_pubid(sess: AsyncSession, pubid: str) -> user_models.User:
    stmt = select(user_models.User).where(user_models.User.id == pubid)
    res = await sess.scalars(stmt)
    return res.one()


async def get_user_by_name(sess: AsyncSession, name: str) -> user_models.User:
    stmt = select(user_models.User).where(user_models.User.name == name)
    res = await sess.scalars(stmt)
    return res.one()


async def get_user_with_items(sess: AsyncSession, pubid: str) -> user_models.User:
    stmt = (
        select(user_models.User)
        .options(joinedload(user_models.User.items))
        .where(user_models.User.id == pubid)
    )
    res = await sess.execute(stmt)
    return res.unique().scalars().one()


async def create_user(
    sess: AsyncSession,
    name: str,
    password_hash: str | None = None,
    fullname: str | None = None,
) -> user_models.User:
    params = {"name": name, "fullname": fullname, "password_hash": password_hash}
    stmt = insert(user_models.User).returning(user_models.User)
    res = await sess.scalars(stmt, params)
    return res.one()


async def update_user(
    sess: AsyncSession, pubid: str, fullname: str | None = None
) -> user_models.User:
    params = {"fullname": fullname}
    stmt = (
        update(user_models.User)
        .where(user_models.User.id == pubid)
        .returning(user_models.User)
    )
    res = await sess.scalars(stmt, params)
    return res.one()


async def delete_user(sess: AsyncSession, pubid: str):
    stmt = delete(user_models.User).where(user_models.User.id == pubid)
    await sess.execute(stmt)
