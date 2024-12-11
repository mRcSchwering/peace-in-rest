from typing import Sequence
import logging
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from app.database.models.users import User

log = logging.getLogger(__name__)


def get_all_users(sess: Session) -> Sequence[User]:
    stmt = select(User)
    users = sess.scalars(stmt).all()
    return users


def create_user(sess: Session, name: str, fullname: str | None) -> User:
    params = {"name": name, "fullname": fullname}
    with sess.begin():
        stmt = insert(User).returning(User)
        user = sess.scalars(stmt, params).one()
    return user


def update_user(sess: Session, id: int, fullname: str | None) -> User:
    params = {"fullname": fullname}
    with sess.begin():
        stmt = update(User).where(User.id == id).returning(User)
        user = sess.scalars(stmt, params).one()
    return user


def delete_user(sess: Session, id: int):
    with sess.begin():
        stmt = delete(User).where(User.id == id)
        sess.execute(stmt)
