from typing import Sequence
from pydantic import BaseModel, Field
from app.database.models import user_models
from .items import ItemResponse

# TODO: check UUIDs in pydantic (have fixed character length)


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
    password: str
    fullname: str | None = None


class UpdateUserPayload(BaseModel):
    fullname: str | None = None
