from typing import Optional
from uuid import UUID

from app.db.daos.player_dao import PlayerDAO
from app.db.db_connection_handler import DBConnectionHandler
from app.domain.player import Player
from app.dto.player_dto import PlayerCreateDTO, PlayerDTO


class PlayerService:
    def __init__(self, db_handler: DBConnectionHandler):
        self._player_dao = PlayerDAO(db_handler)

    def add_player(self, player_create_dto: PlayerCreateDTO) -> Player:
        player = self._player_dao.add(
            first_name=player_create_dto.first_name,
            last_name=player_create_dto.last_name,
            email=player_create_dto.email,
            phone=player_create_dto.phone_number,
        )

        return Player.from_db_model(player)

    def get_player_by_id(self, player_id: UUID) -> Optional[Player]:
        player_dao = self._player_dao.get_by_id(str(player_id))
        if player_dao is None:
            return None
        return Player.from_db_model(player_dao)

    def get_players(self, constraints: dict) -> list[PlayerDTO]:
        pass

    def register_player_to_game(self, player_id: UUID, game_id: UUID) -> bool:
        pass
