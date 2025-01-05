import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth import (
    verify_password,
    decode_access_token,
    create_access_token,
    create_refresh_token,
)
from app.database.models import user_models
from app.services import user_service


log = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


_token_validation_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token",
    headers={"WWW-Authenticate": "Bearer"},
)

_wrong_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


# TODO: claims as Model?
def get_token_claims(token: str) -> dict:
    """Parse and verify token, raise HTTPException if token invalid."""
    try:
        claims = decode_access_token(token=token)
    except InvalidTokenError as err:
        log.warning("Invalid token was provided: %r", err)
        raise _token_validation_exception from err
    if "sub" not in claims:
        log.warning("Invalid token was provided: 'sub' claim not in token.")
        raise _token_validation_exception
    return claims


def generate_user_tokens(user_pubid: str) -> tuple[str, str]:
    """Returns access_token, refresh_token for user"""
    log.info("Generating access and refresh token for %s", user_pubid)
    access_token = create_access_token(sub=user_pubid)
    refresh_token = create_refresh_token(sub=user_pubid)
    return access_token, refresh_token


async def check_refresh_token(sess: AsyncSession, token: str) -> user_models.User:
    """Returns user, aises HTTPException is anything is wrong"""
    log.info("Checking refresh token")
    claims = get_token_claims(token=token)

    try:
        return await user_service.get_user_by_pubid(sess=sess, pubid=claims["sub"])
    except NoResultFound as err:
        log.warning("Invalid token was provided: 'sub'=%r not found", claims["sub"])
        raise _token_validation_exception from err


async def check_login_credentials(
    sess: AsyncSession, username: str, password: str
) -> user_models.User:
    """Returns user, aises HTTPException is anything is wrong"""
    log.info("Checking login credentials for %s", username)
    try:
        user = await user_service.get_user_by_name(sess=sess, name=username)
    except NoResultFound as err:
        log.warning("Login for %s failed: user not found", username)
        raise _wrong_credentials_exception from err

    if user.password_hash is None:
        log.warning("Login for %s failed: user does not have password hash", username)
        raise _wrong_credentials_exception

    if not verify_password(pw=password, pwhash=user.password_hash):
        log.warning("Login for %s failed: provided password is wrong", username)
        raise _wrong_credentials_exception

    return user
