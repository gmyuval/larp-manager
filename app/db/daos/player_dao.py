import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.db.db_connection_handler import DBConnectionHandler
from app.db.models.game import GameDBModel
from app.db.models.player import PlayerDBModel
from app.dto.player_dto import PlayerDTO
from app.exceptions import PlayerAlreadyExists

logger = logging.getLogger(__name__)


class PlayerDAO:
    def __init__(self, db_handler: DBConnectionHandler):
        self._db_handler = db_handler

    def add(self, first_name: str, last_name: str, email: str, phone: Optional[str]) -> PlayerDBModel:
        new_player = PlayerDBModel(first_name=first_name, last_name=last_name, email=email, phone=phone)
        with self._db_handler.session_scope() as session:
            existing_player = session.query(PlayerDBModel).filter(
                PlayerDBModel.first_name == first_name,
                PlayerDBModel.last_name == last_name,
                PlayerDBModel.email == email
            ).first()
            if existing_player:
                logger.debug(f"Player with name {first_name} {last_name} and email {email} already exists")
                raise PlayerAlreadyExists(f"Player with name {first_name} {last_name} and email {email} already exists")
            session.add(new_player)
            session.commit()
        return new_player

    def get_by_id(self, player_id: str) -> Optional[PlayerDBModel]:
        with self._db_handler.session_scope() as session: # type: Session
            player = session.query(PlayerDBModel).filter_by(id=str(player_id)).first()
            if not player:
                logger.debug(f"Player with id {player_id} not found")
            return player

    def get_players(self) -> list[PlayerDBModel]:
        pass

    def upsert(self, player: PlayerDTO) -> Optional[PlayerDBModel]:
        player_model = PlayerDBModel.from_dto(player)
        with self._db_handler.session_scope() as session: # type: Session
            existing_player = session.query(PlayerDBModel).filter_by(id=player_model.id).first()
            if existing_player:
                if player_model.name != existing_player.name or player_model.id != existing_player.id:
                    logger.warning(f"Player name or id cannot be updated.")
                    player_model = None
                else:
                    existing_player.email = player_model.email
                    existing_player.phone = player_model.phone
            else:
                session.add(player_model)
            session.commit()
        return existing_player or player_model

    def add_player_to_game(self, player_id: str, game_id: str) -> bool:
        player = self.get_by_id(player_id)
        with self._db_handler.session_scope() as session: # type: Session
            game = session.query(GameDBModel).filter(GameDBModel.id == game_id).first()
            if not player or not game:
                return False
            if game not in player.registered_games:
                player.registered_games.append(game)
            return True