from datetime import date
from typing import Optional
from uuid import UUID, uuid4


class Game:
    def __init__(self, *, name: str, game_date: date, description: str, game_id: Optional[UUID] = None) -> None:
        self.uuid = game_id if game_id else uuid4()
        self.name = name
        self.game_date = game_date
        self.description = description
