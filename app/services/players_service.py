from typing import Optional
from uuid import UUID

from app.db.daos.player_dao import PlayerDAO
from app.db.db_connection_handler import DBConnectionHandler
from app.models.domain.player import Player
from app.models.dto.player_requests_dtos import PlayerCreateDTO, PlayersGetDTO
from app.models.filter import Filter, FilterModel, Operator


class PlayersService:
    def __init__(self, db_handler: DBConnectionHandler):
        self._player_dao = PlayerDAO(db_handler)

    def add_player(self, player_create_dto: PlayerCreateDTO) -> Player:
        player = self._player_dao.add(
            first_name=player_create_dto.first_name,
            last_name=player_create_dto.last_name,
            full_name=self.create_full_name(player_create_dto.first_name, player_create_dto.last_name),
            date_of_birth=player_create_dto.date_of_birth,
            email=player_create_dto.email,
            phone=player_create_dto.phone_number,
        )

        return Player.from_db_model(player)

    @staticmethod
    def create_full_name(first_name: str, last_name: str) -> str:
        return f"{first_name} {last_name}"

    def get_player_by_id(self, player_id: UUID) -> Optional[Player]:
        player_dao = self._player_dao.get_by_id(str(player_id))
        if player_dao is None:
            return None
        return Player.from_db_model(player_dao)

    def get_players_by_filter(self, request_dto: PlayersGetDTO) -> list[Player]:
        """
        Get players from the database with specific filters.
        The method allows for equality tests only. For scanning the DB with conditions use scan_players
        :param request_dto: Request with conditions to be met
        :return: list of players matching the conditions
        """
        request_dict = request_dto.model_dump()
        filters = [
            Filter(db_model=FilterModel.PLAYER, column_name=key, op=Operator.EQ, value=request_dict[key]) for key in request_dict if key != "limit"
        ]
        db_models = self._player_dao.get_players(*filters, limit=request_dto.limit)
        return [Player.from_db_model(db_model) for db_model in db_models]

    def scan_players(self) -> list[Player]:
        return []

    def register_player_to_game(self, player_id: UUID, game_id: UUID) -> bool:
        return False
