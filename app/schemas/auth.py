from pydantic import BaseModel


class RefreshTokenPayload(BaseModel):
    refresh_token: str
    grant_type: str = "refresh_token"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
