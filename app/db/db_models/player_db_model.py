from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db_models.person_db_model import PersonDBModel

if TYPE_CHECKING:
    from app.db.db_models.game_db_model import GameDBModel


class PlayerDBModel(PersonDBModel):
    __tablename__ = "players"

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    registered_games: Mapped[list["GameDBModel"]] = relationship("GameDBModel", secondary="registrations", back_populates="registered_players")

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.full_name})>"
