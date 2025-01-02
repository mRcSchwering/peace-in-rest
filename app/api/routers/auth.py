from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import AsyncSessionDep
from app.modules.auth import create_access_token
from app.schemas.auth import TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenResponse, response_model_exclude_none=True)
async def login_for_access_token(
    session: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    await auth_service.check_login_credentials(
        sess=session, username=form_data.username, password=form_data.password
    )
    token = create_access_token(sub=form_data.username)
    return TokenResponse(access_token=token, token_type="bearer")
