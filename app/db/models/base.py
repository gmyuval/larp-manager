from typing import Any, TypeVar

from sqlalchemy import JSON, Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound="BaseDBModel")


class Base(DeclarativeBase):
    pass


registrations = Table(
    "registrations",
    Base.metadata,
    Column("player_id", ForeignKey("players.id"), primary_key=True),
    Column("game_id", ForeignKey("games.id"), primary_key=True),
)


class BaseDBModel(Base):
    __abstract__ = True
    type_annotation_map = {
        dict[str, Any]: JSON,
        dict[str, str]: JSON,
    }
