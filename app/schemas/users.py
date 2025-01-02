from typing import Sequence, Annotated
from string import ascii_letters
from pydantic import BaseModel, Field, AfterValidator
from app.database.models import user_models
from .items import ItemResponse


def _validate_password(value: str) -> str:
    if len(value) < 8 or len(value) > 50:
        raise ValueError("Password length must be between 8 and 50 characters")
    if set(ascii_letters) & set(value) == set():
        raise ValueError("Password must contain at least 1 character")
    if set(str(d) for d in range(10)) & set(value) == set():
        raise ValueError("Password must contain at least 1 number")
    return value


class A(BaseModel):
    a: Annotated[str, AfterValidator(_validate_password)]


class UserResponse(BaseModel):
    pubid: str
    name: str
    fullname: str | None = None

    @classmethod
    def from_orm(cls, obj: user_models.User):
        return cls(pubid=obj.id, name=obj.name, fullname=obj.fullname)


class UserWithItemsResponse(BaseModel):
    pubid: str
    name: str
    fullname: str | None = None
    items: list[ItemResponse] | None = None

    @classmethod
    def from_orm(cls, obj: user_models.User):
        items = [ItemResponse.from_orm(d) for d in obj.items]
        return cls(pubid=obj.id, name=obj.name, fullname=obj.fullname, items=items)


class UsersResponse(BaseModel):
    users: list[UserResponse]

    @classmethod
    def from_users(cls, users: Sequence[user_models.User]):
        return cls(users=[UserResponse.from_orm(obj=d) for d in users])


class CreateUserPayload(BaseModel):
    name: str = Field(..., max_length=30)
    password: str = Field(..., min_length=8, max_length=50)
    fullname: str | None = None


class UpdateUserPayload(BaseModel):
    fullname: str | None = None
