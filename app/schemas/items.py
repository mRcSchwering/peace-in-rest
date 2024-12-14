from typing import Sequence
import datetime as dt
from pydantic import BaseModel, Field
from app.database.models import item_models


class ItemResponse(BaseModel):
    pubid: str
    name: str
    added: dt.datetime

    @classmethod
    def from_orm(cls, obj: item_models.Item):
        return cls(pubid=obj.id, name=obj.name, added=obj.added)


class ItemsResponse(BaseModel):
    items: list[ItemResponse]

    @classmethod
    def from_items(cls, items: Sequence[item_models.Item]):
        return cls(items=[ItemResponse.from_orm(obj=d) for d in items])


class CreateItemPayload(BaseModel):
    name: str = Field(..., max_length=30)
    user_pubid: str


class UpdateItemPayload(BaseModel):
    added: dt.datetime | None = None
