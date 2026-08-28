from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from madr_api.database import table_registry


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = "novelists"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list[Book]] = relationship(
        back_populates="novelist", default_factory=list
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int]
    novelist_id: Mapped[int] = mapped_column(ForeignKey("novelists.id"), init=False)
    novelist: Mapped[Novelist] = relationship(back_populates="books")


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
