from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth import verify_password
from app.services import user_service
from app.exceptions import LoginFailedWarning


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def check_login_credentials(sess: AsyncSession, username: str, password: str):
    """Raises LoginFailedException if anything is wrong"""
    try:
        user = await user_service.get_user_by_name(sess=sess, name=username)
    except NoResultFound as err:
        raise LoginFailedWarning(
            f"Login for user {username} failed because user doesnt exist"
        ) from err

    if user.password_hash is None:
        raise LoginFailedWarning(
            f"Login for user {username} failed because user doesnt have password hash"
        )

    if not verify_password(pw=password, pwhash=user.password_hash):
        raise LoginFailedWarning(
            f"Login for user {username} failed because supplied password was wrong"
        )
