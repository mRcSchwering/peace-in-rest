# this python file uses the following encoding: utf-8
from typing import List
from pydantic import BaseModel
from fastapi import Query


# Items
class ItemBase(BaseModel):
    title: str = Query(..., description='The Item title')
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Users
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
