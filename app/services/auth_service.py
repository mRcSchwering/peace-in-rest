import logging
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, DBAPIError, MultipleResultsFound
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import JWT_SECRET_KEY
from app.modules.auth import verify_password, decode_token, generate_token
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


@dataclass
class TokenClaims:
    user_pubid: str


def parse_token_claims(token: str) -> TokenClaims:
    """Parse and verify token, raise HTTPException if token invalid."""
    try:
        claims = decode_token(token=token, secret=JWT_SECRET_KEY)
    except InvalidTokenError as err:
        log.warning("Invalid token was provided: %r", err)
        raise _token_validation_exception from err

    try:
        return TokenClaims(user_pubid=claims["sub"])
    except KeyError as err:
        log.warning("Invalid token was provided: %s claim not in token.", err)
        raise _token_validation_exception from err


def generate_user_tokens(user_pubid: str) -> tuple[str, str]:
    """Returns access_token, refresh_token for user"""
    log.info("Generating access and refresh token for %s", user_pubid)
    access_token = generate_token(sub=user_pubid, exp_minutes=60, secret=JWT_SECRET_KEY)
    refresh_token = generate_token(
        sub=user_pubid, exp_minutes=60 * 24, secret=JWT_SECRET_KEY
    )
    return access_token, refresh_token


async def parse_token_and_get_user(sess: AsyncSession, token: str) -> user_models.User:
    """Returns user, aises HTTPException is anything is wrong"""
    log.info("Checking refresh token")
    claims = parse_token_claims(token=token)

    try:
        return await user_service.get_user_by_pubid(sess=sess, pubid=claims.user_pubid)
    except NoResultFound as err:
        log.warning("Invalid token was provided: user %r not found", claims.user_pubid)
        raise _token_validation_exception from err
    except DBAPIError as err:
        log.warning(
            "Login for %s failed: user id not accepted by database", claims.user_pubid
        )
        raise _token_validation_exception from err
    except MultipleResultsFound as err:
        log.warning(
            "Login for %s failed: multiple users with this id found", claims.user_pubid
        )
        raise _token_validation_exception from err


async def check_login_credentials_and_get_user(
    sess: AsyncSession, username: str, password: str
) -> user_models.User:
    """Returns user, aises HTTPException is anything is wrong"""
    log.info("Checking login credentials for %s", username)
    try:
        user = await user_service.get_user_by_name(sess=sess, name=username)
    except NoResultFound as err:
        log.warning("Login for %s failed: user not found", username)
        raise _wrong_credentials_exception from err
    except DBAPIError as err:
        log.warning("Login for %s failed: user name not accepted by database", username)
        raise _wrong_credentials_exception from err
    except MultipleResultsFound as err:
        log.warning(
            "Login for %s failed: multiple users with this name found", username
        )
        raise _wrong_credentials_exception from err

    if user.password_hash is None:
        log.warning("Login for %s failed: user does not have password hash", username)
        raise _wrong_credentials_exception

    if not verify_password(pw=password, pwhash=user.password_hash):
        log.warning("Login for %s failed: provided password is wrong", username)
        raise _wrong_credentials_exception

    return user
