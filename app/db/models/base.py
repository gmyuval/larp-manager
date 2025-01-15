from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import JSON, Column, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
T = TypeVar("T", bound="BaseDBModel")
registrations = Table(
    "registrations",
    Base.metadata,
    Column("player_id", ForeignKey("players.id"), primary_key=True),
    Column("game_id", ForeignKey("games.id"), primary_key=True),
)


class BaseDBModel(Base):
    __abstract__ = True
    type_annotation_map = {dict[str, Any]: JSON}

    @classmethod
    def from_dto(cls: Type[T], dto: BaseModel) -> T:
        raise NotImplementedError
