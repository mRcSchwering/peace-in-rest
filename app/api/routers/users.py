import logging
from fastapi import APIRouter
from app.dependencies import SessionDep
from app.schemas.users import (
    UserResponse,
    CreateUserPayload,
    UpdateUserPayload,
    UsersResponse,
)
from app.services import user_service

log = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("", response_model=UsersResponse, response_model_exclude_none=True)
def get_users(session: SessionDep):
    log.info("Getting all users")
    users = user_service.get_all_users(sess=session)
    return {"users": users}


@router.get("/{pubid}", response_model=UserResponse, response_model_exclude_none=True)
def get_user_by_id(session: SessionDep, pubid: str):
    log.info("Getting user %s", pubid)
    return user_service.get_user(sess=session, pubid=pubid)


@router.post(
    "", response_model=UserResponse, response_model_exclude_none=True, status_code=201
)
def create_user(session: SessionDep, payload: CreateUserPayload):
    log.info("Creating new user")
    return user_service.create_user(
        sess=session, name=payload.name, fullname=payload.fullname
    )


@router.put("/{pubid}", response_model=UserResponse, response_model_exclude_none=True)
def update_user(session: SessionDep, pubid: str, payload: UpdateUserPayload):
    log.info("Updating user %s", pubid)
    return user_service.update_user(
        sess=session, pubid=pubid, fullname=payload.fullname
    )


@router.delete("/{pubid}", response_model_exclude_none=True)
def delete_user(session: SessionDep, pubid: str):
    log.info("Deleting user %s", pubid)
    user_service.delete_user(sess=session, pubid=pubid)
