from fastapi import APIRouter, HTTPException, status
from app.dependencies import AsyncSessionDep, AccessTokenClaimsDep
from app.schemas.users import (
    UserResponse,
    CreateUserPayload,
    UpdateUserPayload,
    UsersResponse,
    UserWithItemsResponse,
)
from app.modules.auth import hash_password
from app.services import user_service


router = APIRouter(prefix="/users")


@router.get("", response_model=UsersResponse, response_model_exclude_none=True)
async def get_users(session: AsyncSessionDep):
    """List all users"""
    users = await user_service.get_all_users(sess=session)
    return UsersResponse.from_users(users=users)


@router.get(
    "/{pubid}",
    response_model=UserResponse | UserWithItemsResponse,
    response_model_exclude_none=True,
)
async def get_user_by_pubid(
    session: AsyncSessionDep, pubid: str, incl_items: bool = False
):
    """Get one user by id"""
    if incl_items:
        user = await user_service.get_user_with_items(sess=session, pubid=pubid)
        return UserWithItemsResponse.from_orm(user)
    user = await user_service.get_user_by_pubid(sess=session, pubid=pubid)
    return UserResponse.from_orm(user)


@router.post(
    "", response_model=UserResponse, response_model_exclude_none=True, status_code=201
)
async def create_user(session: AsyncSessionDep, payload: CreateUserPayload):
    """Create a new user"""
    hashed_password = hash_password(pw=payload.password)

    user = await user_service.create_user(
        sess=session,
        name=payload.name,
        password_hash=hashed_password,
        fullname=payload.fullname,
    )
    return UserResponse.from_orm(user)


@router.put("/{pubid}", response_model=UserResponse, response_model_exclude_none=True)
async def update_user(
    session: AsyncSessionDep,
    claims: AccessTokenClaimsDep,
    pubid: str,
    payload: UpdateUserPayload,
):
    """Update an existing user"""
    if claims.user_pubid != pubid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user = await user_service.update_user(
        sess=session, pubid=pubid, fullname=payload.fullname
    )
    return UserResponse.from_orm(user)


@router.delete("/{pubid}", response_model_exclude_none=True)
async def delete_user(
    session: AsyncSessionDep, claims: AccessTokenClaimsDep, pubid: str
):
    """Delete an existing user"""
    if claims.user_pubid != pubid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await user_service.delete_user(sess=session, pubid=pubid)
