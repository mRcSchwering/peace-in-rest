from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import AsyncSessionDep
from app.modules.auth import create_access_token, verify_password
from app.schemas.auth import TokenResponse
from app.services import user_service

router = APIRouter(prefix="/auth")

# TODO: in service?
# TODO: logs


@router.post("/token", response_model=TokenResponse, response_model_exclude_none=True)
async def login_for_access_token(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await user_service.get_user_by_name(sess=session, name=form_data.username)
    if not user:
        raise exc

    if user.password_hash is None:
        raise exc

    if not verify_password(pw=form_data.password, pwhash=user.password_hash):
        raise exc

    token = create_access_token(sub=user.name)
    return TokenResponse(access_token=token, token_type="bearer")
