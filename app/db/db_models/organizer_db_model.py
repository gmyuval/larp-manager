from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.db.db_models.person_db_model import PersonDBModel

if TYPE_CHECKING:
    from app.db.db_models.game_db_model import GameDBModel


class OrganizerDBModel(PersonDBModel):
    __tablename__ = "organizers"

    organized_games: Mapped[list["GameDBModel"]] = relationship("Game", secondary="game_orgs", back_populates="organizers")
