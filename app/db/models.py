# this python file uses the following encoding: utf-8
from pydantic import BaseModel
from typing import List, Dict


class Date(BaseModel):
    id: int
    date: dt.date  # pydantic can interpret many typical classes already


# below I use this model as both response model and payload definition
class Animal(BaseModel):
    id: int = None # by giving it a default value, it is not a required field
    name: str  # this field is required
    types: List[str] = ['furry']  # this list is precisely defined as a `list` of `str` (any list would be `list`)
    info: dict = None  # this one is just any `dict` (precise would be `Dict[str, int]`)
