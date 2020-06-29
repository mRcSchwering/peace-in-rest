# this python file uses the following encoding: utf-8
"""API Models (here = schemas)

API models are called schemas here to not confuse them with database models.
Can be used for defining payloads and marshalling responses.
Use `Query()` to add some description to a field.
`Query(...)` for required value, `Query(None)` for not required (default=None).
Define class Config with `orm_mode = True` to make schema understand
SQLAlchemy model objects.
"""
from typing import List
from pydantic import BaseModel
from fastapi import Query


class OrmBase(BaseModel):

    class Config:
        orm_mode = True


# Items
class ItemBase(OrmBase):
    title: str = Query(..., description='The Item title')
    description: str = None


class ItemCreate(ItemBase):
    # works same with GET query params
    asd1: str = Query(..., description='This is not optional')
    asd2: str = Query(None, description='This is optional')
    asd3: str = Query("a", enum=["a", "b"], description='Selection')


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Users
class UserBase(OrmBase):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
