import uuid
from typing import Type

from sqlalchemy import Computed, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseDBModel, T
from app.dto.player_dto import PlayerDTO


class PlayerDBModel(BaseDBModel):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(
        String, Computed("first_name || ' ' || last_name", persisted=True), nullable=False
    )
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(index=True, nullable=True)
    registered_games: Mapped[list["GameDBModel"]] = relationship(
        "Game", secondary="registrations", back_populates="players"
    )

    @classmethod
    def from_dto(cls: Type[T], dto: "PlayerDTO") -> "PlayerDBModel":
        return cls(
            id=str(dto.id), name=dto.name.full_name, email=dto.contact_details.email, phone=dto.contact_details.phone
        )

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name})>"
