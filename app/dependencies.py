from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import SessionFact


async def _get_db_session():
    async with SessionFact() as session:
        yield session
        await session.commit()  # automatically commit in request context


SessionDep = Annotated[AsyncSession, Depends(_get_db_session)]
