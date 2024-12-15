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
async def get_users(session: SessionDep):
    log.info("Getting all users")
    users = await user_service.get_all_users(sess=session)
    return UsersResponse.from_users(users=users)


@router.get("/{pubid}", response_model=UserResponse, response_model_exclude_none=True)
async def get_user_by_id(session: SessionDep, pubid: str):
    log.info("Getting user %s", pubid)
    user = await user_service.get_user(sess=session, pubid=pubid)
    return UserResponse.from_orm(user)


@router.post(
    "", response_model=UserResponse, response_model_exclude_none=True, status_code=201
)
async def create_user(session: SessionDep, payload: CreateUserPayload):
    log.info("Creating new user")
    user = await user_service.create_user(
        sess=session, name=payload.name, fullname=payload.fullname
    )
    return UserResponse.from_orm(user)


@router.put("/{pubid}", response_model=UserResponse, response_model_exclude_none=True)
async def update_user(session: SessionDep, pubid: str, payload: UpdateUserPayload):
    log.info("Updating user %s", pubid)
    user = await user_service.update_user(
        sess=session, pubid=pubid, fullname=payload.fullname
    )
    return UserResponse.from_orm(user)


@router.delete("/{pubid}", response_model_exclude_none=True)
async def delete_user(session: SessionDep, pubid: str):
    log.info("Deleting user %s", pubid)
    await user_service.delete_user(sess=session, pubid=pubid)
