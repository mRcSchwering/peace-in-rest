# this python file uses the following encoding: utf-8
"""All CRUD Operations

Nice trick: `models.Item(**item.dict(), owner_id=user_id)`
            where item is a schema (pydantic model)
"""
from typing import List
from sqlalchemy.orm import Session
from app.db import models


# User
def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, **_) -> models.User:
    db_user = models.User(email=email, hashed_password='notreallyhashed')
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Items
def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, title: str, description: str, user_id: int, **_) -> models.Item:
    db_item = models.Item(
        title=title, description=description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
