from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from app.db.db_models.game_db_model import GameDBModel


class Game:
    def __init__(
        self,
        *,
        name: str,
        game_date: date,
        description: str,
        registration_start_date: date,
        registration_end_date: date,
        game_id: Optional[UUID] = None,
    ) -> None:
        self.id = game_id if game_id else uuid4()
        self.name = name
        self.game_date = game_date
        self.description = description
        self.registration_start_date = registration_start_date
        self.registration_end_date = registration_end_date

    @classmethod
    def from_db_model(cls, model: GameDBModel) -> "Game":
        return cls(
            game_id=UUID(model.id),
            name=model.name,
            game_date=model.game_start_date,
            description=model.description,
            registration_start_date=model.registration_open_date,
            registration_end_date=model.registration_close_date,
        )
