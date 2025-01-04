from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import AsyncSessionDep
from app.modules.auth import create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse, RefreshTokenPayload
from app.services import auth_service

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenResponse, response_model_exclude_none=True)
async def login_to_get_access_token(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await auth_service.check_login_credentials(
        sess=session, username=form_data.username, password=form_data.password
    )

    access_token = create_access_token(sub=user.name)
    refresh_token = create_refresh_token(sub=user.name)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse, response_model_exclude_none=True)
async def refresh_access_token(session: AsyncSessionDep, form_data=RefreshTokenPayload):
    user = await auth_service.check_refresh_token(
        sess=session, token=form_data.refresh_token
    )

    access_token = create_access_token(sub=user.name)
    refresh_token = create_refresh_token(sub=user.name)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
