from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionFact


def _get_db_session():
    with SessionFact() as session:
        yield session
        session.commit()  # automatically commit in request context


SessionDep = Annotated[Session, Depends(_get_db_session)]
