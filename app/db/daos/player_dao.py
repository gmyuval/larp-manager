import logging
from datetime import date
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Query, Session

from app.db.daos.base_dao import BaseDAO
from app.db.db_models.game_db_model import GameDBModel
from app.db.db_models.player_db_model import PlayerDBModel
from app.exceptions import PlayerAlreadyExists, PlayerNotFound
from app.models.domain import Player
from app.models.filter import Filter

logger = logging.getLogger(__name__)


class PlayerDAO(BaseDAO):
    def add(
        self,
        *,
        first_name: str,
        last_name: str,
        full_name: str,
        email: str,
        date_of_birth: Optional[date],
        phone: Optional[str],
        pid: Optional[str] = None,
    ) -> PlayerDBModel:
        new_player = PlayerDBModel(
            id=pid, first_name=first_name, last_name=last_name, full_name=full_name, email=email, phone=phone, date_of_birth=date_of_birth
        )
        with self._db_handler.session_scope() as session:  # type: Session
            existing_player = (
                session.query(PlayerDBModel)
                .filter(
                    PlayerDBModel.first_name == first_name,
                    PlayerDBModel.last_name == last_name,
                    PlayerDBModel.email == email,
                )
                .first()
            )
            if existing_player:
                logger.debug(f"Player with name {first_name} {last_name} and email {email} already exists")
                raise PlayerAlreadyExists(f"Player with name {first_name} {last_name} and email {email} already exists")
            session.add(new_player)
            session.commit()
        return new_player

    def get_by_id(self, player_id: str) -> Optional[PlayerDBModel]:
        with self._db_handler.session_scope() as session:  # type: Session
            player = session.query(PlayerDBModel).filter_by(id=str(player_id)).first()
            if not player:
                logger.debug(f"Player with id {player_id} not found")
            return player

    def get_players(self, *filters: Filter, limit: Optional[int] = None) -> list[PlayerDBModel]:
        if not filters:
            raise ValueError("At least one filter is required")
        with self._db_handler.session_scope() as session:  # type: Session
            query: Query[PlayerDBModel] = session.query(PlayerDBModel)  # type: ignore
            for player_filter in filters:
                query = query.filter(player_filter.to_condition())
            if limit:
                query = query.limit(limit)
            return query.all()

    def update(self, player_id: str, **fields_to_update: dict[str, Any]) -> None:
        with self._db_handler.session_scope() as session:  # type: Session
            stmt = select(PlayerDBModel).filter_by(id=player_id)
            player = session.execute(stmt).first()
            if not player:
                raise PlayerNotFound(f"Player with id {player_id} not found")
            valid_columns = {column.key: column.type for column in PlayerDBModel.__table__.columns}  # type: ignore
            for column, value in fields_to_update.items():
                if column not in valid_columns:
                    raise ValueError(f"Invalid column {column}")
                if not isinstance(value, valid_columns[column].python_type):
                    raise TypeError(f"column {column} expects value of type {valid_columns[column].python_type}. received {type(value)}")
                setattr(player, column, value)
            session.commit()

    def upsert(self, player: Player) -> Optional[PlayerDBModel]:
        player_model = player.to_db_model()
        with self._db_handler.session_scope() as session:  # type: Session
            existing_player = session.query(PlayerDBModel).filter_by(id=player_model.id).first()
            if existing_player:
                if player_model.full_name != existing_player.full_name or player_model.id != existing_player.id:
                    logger.warning("Player full name or id cannot be updated.")
                    returned_model = None
                else:
                    existing_player.email = player_model.email
                    existing_player.phone = player_model.phone
                    existing_player.date_of_birth = player_model.date_of_birth
                    returned_model = existing_player
            else:
                returned_model = player_model
                session.add(player_model)
            session.commit()
        return returned_model

    def add_player_to_game(self, player_id: str, game_id: str) -> bool:
        player = self.get_by_id(player_id)
        with self._db_handler.session_scope() as session:  # type: Session
            game = session.query(GameDBModel).filter(GameDBModel.id == game_id).first()
            if not player or not game:
                return False
            if game not in player.registered_games:
                player.registered_games.append(game)
            return True
