from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import AsyncSessionDep
from app.schemas.auth import TokenResponse, RefreshTokenPayload
from app.services import auth_service

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenResponse, response_model_exclude_none=True)
async def login(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Login to get access and refresh tokens"""
    user = await auth_service.check_login_credentials(
        sess=session, username=form_data.username, password=form_data.password
    )

    access_token, refresh_token = auth_service.generate_user_tokens(user_pubid=user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse, response_model_exclude_none=True)
async def refresh(session: AsyncSessionDep, form_data=RefreshTokenPayload):
    """Get new refresh and access tokens using a valid refresh token"""
    user = await auth_service.check_refresh_token(
        sess=session, token=form_data.refresh_token
    )

    access_token, refresh_token = auth_service.generate_user_tokens(user_pubid=user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
