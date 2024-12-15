from typing import Sequence
import logging
import datetime as dt
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import item_models

log = logging.getLogger(__name__)


async def get_all_items(
    sess: AsyncSession, user_pubid: str
) -> Sequence[item_models.Item]:
    stmt = select(item_models.Item).where(item_models.Item.user_id == user_pubid)
    res = await sess.scalars(stmt)
    return res.all()


async def get_item(sess: AsyncSession, pubid: str) -> item_models.Item:
    stmt = select(item_models.Item).where(item_models.Item.id == pubid)
    res = await sess.scalars(stmt)
    return res.one()


async def create_item(
    sess: AsyncSession, user_pubid: str, name: str
) -> item_models.Item:
    params = {"name": name, "user_id": user_pubid}
    stmt = insert(item_models.Item).returning(item_models.Item)
    res = await sess.scalars(stmt, params)
    return res.one()


async def update_item(
    sess: AsyncSession, pubid: str, added: dt.datetime | None = None
) -> item_models.Item:
    params = {"added": added}
    stmt = (
        update(item_models.Item)
        .where(item_models.Item.id == pubid)
        .returning(item_models.Item)
    )
    res = await sess.scalars(stmt, params)
    return res.one()


async def delete_item(sess: AsyncSession, pubid: str):
    stmt = delete(item_models.Item).where(item_models.Item.id == pubid)
    await sess.execute(stmt)
