from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import AsyncSessionMaker


async def _get_db_session():
    async with AsyncSessionMaker() as session:
        yield session
        await session.commit()  # automatically commit in request context


AsyncSessionDep = Annotated[AsyncSession, Depends(_get_db_session)]
