from typing import Sequence
import logging
import datetime as dt
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from app.database.models import item_models

log = logging.getLogger(__name__)


def get_all_items(sess: Session, user_pubid: str) -> Sequence[item_models.Item]:
    stmt = select(item_models.Item).where(item_models.Item.user_id == user_pubid)
    return sess.scalars(stmt).all()


def get_item(sess: Session, pubid: str) -> item_models.Item:
    stmt = select(item_models.Item).where(item_models.Item.id == pubid)
    return sess.scalars(stmt).one()


def create_item(sess: Session, user_pubid: str, name: str) -> item_models.Item:
    params = {"name": name, "user_id": user_pubid}
    stmt = insert(item_models.Item).returning(item_models.Item)
    item = sess.scalars(stmt, params).one()
    return item


def update_item(
    sess: Session, pubid: str, added: dt.datetime | None = None
) -> item_models.Item:
    params = {"added": added}
    stmt = (
        update(item_models.Item)
        .where(item_models.Item.id == pubid)
        .returning(item_models.Item)
    )
    return sess.scalars(stmt, params).one()


def delete_item(sess: Session, pubid: str):
    stmt = delete(item_models.Item).where(item_models.Item.id == pubid)
    sess.execute(stmt)
