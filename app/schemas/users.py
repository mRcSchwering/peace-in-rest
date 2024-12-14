from typing import Sequence
from pydantic import BaseModel, Field
from app.database.models import user_models


class UserResponse(BaseModel):
    pubid: str
    name: str
    fullname: str | None

    @classmethod
    def from_orm(cls, obj: user_models.User):
        return cls(pubid=obj.id, name=obj.name, fullname=obj.fullname)


class UsersResponse(BaseModel):
    users: list[UserResponse]

    @classmethod
    def from_users(cls, users: Sequence[user_models.User]):
        return cls(users=[UserResponse.from_orm(obj=d) for d in users])


class CreateUserPayload(BaseModel):
    name: str = Field(..., max_length=30)
    fullname: str | None = None


class UpdateUserPayload(BaseModel):
    fullname: str | None = None
