from typing import Annotated
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import AsyncSessionMaker
from app.services import auth_service

log = logging.getLogger(__name__)


async def _get_db_session():
    async with AsyncSessionMaker() as session:
        yield session
        await session.commit()  # automatically commit in request context


async def _get_token_claims(
    token: Annotated[str, Depends(auth_service.oauth2_scheme)]
) -> dict:
    return auth_service.get_token_claims(token=token)


AsyncSessionDep = Annotated[AsyncSession, Depends(_get_db_session)]
AccessTokenClaimsDep = Annotated[dict, Depends(_get_token_claims)]
