from typing import TYPE_CHECKING
import datetime as dt
from sqlalchemy import UUID, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from app.modules.utils import utcnow
from .common import Base

if TYPE_CHECKING:
    from .user_models import User


class Item(Base):
    __tablename__ = "item"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(30))
    added: Mapped[dt.datetime] = mapped_column(DateTime, default=utcnow)

    user: Mapped["User"] = relationship(back_populates="items")
