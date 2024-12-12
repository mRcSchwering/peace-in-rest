from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    pubid: str
    name: str
    fullname: str | None


class UsersResponse(BaseModel):
    users: list[UserResponse]


class CreateUserPayload(BaseModel):
    name: str = Field(..., max_length=10)
    fullname: str | None = None


class UpdateUserPayload(BaseModel):
    fullname: str | None = None
