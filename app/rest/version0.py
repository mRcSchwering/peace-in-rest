# this python file uses the following encoding: utf-8
"""Endpoints for this namespace

Has to be importet and included to the app object in app.py.
Use schemas for payloads and response marshalling, crud for DB operations.
A database session has to be added `Depends(get_db)`.
In SwaggerUI function names = short descriptions, docstrings = long descriptions.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import exceptions
from app.db import get_db, crud
from app.rest import schemas

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is not None:
        raise exceptions.AlreadyExists()
    return crud.create_user(db=db, **user.dict())


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise exceptions.NoResultFound()
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, user_id=user_id, **item.dict())


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/greet")
async def greetings(
        name: str = Query(..., description='Whats your name?'),
        db: Session = Depends(get_db)):
    """Greetings..."""
    return 'hi ' + name
