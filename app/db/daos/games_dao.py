from datetime import date
from typing import Optional
from uuid import UUID

from app.db.daos.base_dao import BaseDAO
from app.db.models.game_db_model import GameDBModel


class GamesDAO(BaseDAO):
    def add(
        self,
        *,
        name: str,
        description: str,
        game_date: date,
        registration_constraints: dict[str, str],
        game_id: Optional[UUID] = None,
        overwrite_existing: bool = False,
    ) -> GameDBModel:
        game = GameDBModel(
            id=str(game_id) if game_id else None,
            name=name,
            description=description,
            constraints=registration_constraints,
            game_date=game_date,
        )
        with self._db_handler.session_scope() as session:
            if overwrite_existing:
                session.merge(game)
            else:
                session.add(game)

        return game
