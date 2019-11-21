# this python file uses the following encoding: utf-8
import logging
import app.api.params as params
import app.db.methods as methods
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/greet")
async def greetings(
        name: str = params.name,
        db: Session = Depends(get_db)):
    """Greetings..."""
    return methods.greet(name)
