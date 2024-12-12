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


@router.get("/{id}", response_model=UserResponse, response_model_exclude_none=True)
def get_user_by_id(session: SessionDep, id: int):
    log.info("Getting user %s", id)
    return user_service.get_user_by_id(sess=session, id=id)


@router.post(
    "", response_model=UserResponse, response_model_exclude_none=True, status_code=201
)
def create_user(session: SessionDep, payload: CreateUserPayload):
    log.info("Creating new user")
    return user_service.create_user(
        sess=session, name=payload.name, fullname=payload.fullname
    )


@router.put("/{id}", response_model=UserResponse, response_model_exclude_none=True)
def update_user(session: SessionDep, id: int, payload: UpdateUserPayload):
    log.info("Updating user %s", id)
    return user_service.update_user(sess=session, id=id, fullname=payload.fullname)


@router.delete("/{id}", response_model_exclude_none=True)
def delete_user(session: SessionDep, id: int):
    log.info("Deleting user %s", id)
    user_service.delete_user(sess=session, id=id)
