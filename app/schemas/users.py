from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    fullname: str | None


class CreateUserPayload(BaseModel):
    name: str
    fullname: str | None = None


class UpdateUserPayload(BaseModel):
    fullname: str | None = None
