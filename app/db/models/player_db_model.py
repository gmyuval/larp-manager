import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Computed, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseDBModel

if TYPE_CHECKING:
    from app.db.models.game_db_model import GameDBModel


class PlayerDBModel(BaseDBModel):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(String, Computed("first_name || ' ' || last_name", persisted=True), nullable=False)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(index=True, nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    registered_games: Mapped[list["GameDBModel"]] = relationship("Game", secondary="registrations", back_populates="players")

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.full_name})>"
