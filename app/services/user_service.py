from typing import Sequence
import logging
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from app.database.models import user_models

log = logging.getLogger(__name__)


def get_all_users(sess: Session) -> Sequence[user_models.User]:
    stmt = select(user_models.User)
    users = sess.scalars(stmt).all()
    return users


def create_user(sess: Session, name: str, fullname: str | None) -> user_models.User:
    params = {"name": name, "fullname": fullname}
    with sess.begin():
        stmt = insert(user_models.User).returning(user_models.User)
        user = sess.scalars(stmt, params).one()
    return user


def update_user(sess: Session, id: int, fullname: str | None) -> user_models.User:
    params = {"fullname": fullname}
    with sess.begin():
        stmt = (
            update(user_models.User)
            .where(user_models.User.id == id)
            .returning(user_models.User)
        )
        user = sess.scalars(stmt, params).one()
    return user


def delete_user(sess: Session, id: int):
    with sess.begin():
        stmt = delete(user_models.User).where(user_models.User.id == id)
        sess.execute(stmt)
