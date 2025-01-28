from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.daos.base_dao import BaseDAO
from app.db.db_models.game_db_model import GameDBModel


class GamesDAO(BaseDAO):
    def add(
        self,
        *,
        name: str,
        description: Optional[str],
        game_date: date,
        registration_constraints: dict[str, str],
        game_end_date: date | None = None,
        game_id: Optional[UUID] = None,
        registration_open_date: Optional[date] = None,
        registration_close_date: Optional[date] = None,
        overwrite_existing: bool = False,
    ) -> GameDBModel:
        game = GameDBModel(
            id=str(game_id) if game_id else None,
            name=name,
            description=description,
            constraints=registration_constraints,
            game_start_date=game_date,
            game_end_date=game_end_date,
            active=True,
            registration_open_date=registration_open_date if registration_open_date else date.today(),
            registration_close_date=registration_close_date if registration_close_date else game_date,
        )
        with self._db_handler.session_scope() as session:  # type: Session
            # In case the overwrite_existing flag is set, we do not want to keep any info from existing game.
            # This option is not intended to be used as game update.
            if overwrite_existing:
                existing_game = session.query(GameDBModel).filter(GameDBModel.name == name).one_or_none()
                if existing_game:
                    session.delete(existing_game)
            session.add(game)

        return game

    def get_by_id(self, game_id: UUID) -> Optional[GameDBModel]:
        with self._db_handler.session_scope() as session:  # type: Session
            return session.query(GameDBModel).filter(GameDBModel.id == game_id).one_or_none()
