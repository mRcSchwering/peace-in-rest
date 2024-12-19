from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from app.database import AsyncSessionMaker
from app.modules.auth import oauth2_scheme, decode_access_token

# TODO: logging


async def _get_db_session():
    async with AsyncSessionMaker() as session:
        yield session
        await session.commit()  # automatically commit in request context


async def _get_token_claims(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        return decode_access_token(token=token)
    except InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


AsyncSessionDep = Annotated[AsyncSession, Depends(_get_db_session)]
AccessTokenClaimsDep = Annotated[dict, Depends(_get_token_claims)]
