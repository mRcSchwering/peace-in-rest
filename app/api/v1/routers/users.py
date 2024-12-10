import logging
from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies import SessionDep
from app.database.models.users import User

log = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("")
def get_users(session: SessionDep):
    stmt = select(User)
    users = session.scalars(stmt).all()
    log.info("users: %r", users)
    return users


@router.post("")
def create_user(session: SessionDep):
    log.info("Start transaction")
    with session.begin():
        user = User(name="asd", fullname="asdf")
        session.add(user)
        session.flush()
        log.info("Created user: %r", user.id)
        log.info("Commit transaction")
    return user
