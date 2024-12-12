from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionFact


def _get_session():
    with SessionFact() as session:
        yield session


SessionDep = Annotated[Session, Depends(_get_session)]