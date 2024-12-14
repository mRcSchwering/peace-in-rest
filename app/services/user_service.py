from typing import Sequence
import logging
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from app.database.models import user_models

log = logging.getLogger(__name__)


def get_all_users(sess: Session) -> Sequence[user_models.User]:
    stmt = select(user_models.User)
    return sess.scalars(stmt).all()


def get_user(sess: Session, pubid: str) -> user_models.User:
    stmt = select(user_models.User).where(user_models.User.id == pubid)
    return sess.scalars(stmt).one()


def create_user(
    sess: Session, name: str, fullname: str | None = None
) -> user_models.User:
    params = {"name": name, "fullname": fullname}
    stmt = insert(user_models.User).returning(user_models.User)
    return sess.scalars(stmt, params).one()


def update_user(
    sess: Session, pubid: str, fullname: str | None = None
) -> user_models.User:
    params = {"fullname": fullname}
    stmt = (
        update(user_models.User)
        .where(user_models.User.id == pubid)
        .returning(user_models.User)
    )
    return sess.scalars(stmt, params).one()


def delete_user(sess: Session, pubid: str):
    stmt = delete(user_models.User).where(user_models.User.id == pubid)
    sess.execute(stmt)
