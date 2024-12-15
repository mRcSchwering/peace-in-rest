from typing import TYPE_CHECKING
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import uuid
from .common import Base

if TYPE_CHECKING:
    from .item_models import Item


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    # prevent accidentally lazy loading relationships (lazy="raise")
    items: Mapped[list["Item"]] = relationship(
        back_populates="user", cascade="all,delete-orphan", lazy="raise"
    )

    def __str__(self):
        return f"User(name={self.name})"
