from sqlalchemy import ForeignKey
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import uuid
from .common import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    pubid: Mapped[str] = mapped_column(
        UUID(as_uuid=False), unique=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    items: Mapped[list["Item"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="items")
