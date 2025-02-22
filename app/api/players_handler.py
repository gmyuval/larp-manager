import logging
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.exceptions import BadId, PlayerAlreadyExists, PlayerNotFound
from app.models.dto.player_dto import PlayerDTO
from app.models.dto.player_requests_dtos import PlayerCreateDTO, PlayersGetDTO
from app.services.players_service import PlayersService

logger = logging.getLogger(__name__)


class PlayersController:
    def __init__(self, players_service: PlayersService):
        self._players_service = players_service
        self.router = self._create_router()

    def _create_router(self) -> APIRouter:
        router = APIRouter(prefix="/players")
        router.add_api_route(path="/{player_id}", methods=["GET"], endpoint=self.get_player)
        router.add_api_route(path="/by_criteria", methods=["POST"], endpoint=self.get_players_by_criteria)
        router.add_api_route(path="/add_player", methods=["POST"], endpoint=self.add_player, response_model=PlayerDTO)
        return router

    def get_player(self, player_id: str) -> Optional[PlayerDTO]:
        try:
            player_uuid = uuid.UUID(player_id)
        except ValueError as e:
            raise BadId("Invalid player id") from e
        player = self._players_service.get_player_by_id(player_uuid)
        if not player:
            raise PlayerNotFound()
        return player.to_dto()

    def get_players_by_criteria(self, get_dto: PlayersGetDTO) -> list[PlayerDTO]:
        players = self._players_service.get_players_by_filter(get_dto)
        return [player.to_dto() for player in players]

    def add_player(self, req: PlayerCreateDTO) -> PlayerDTO:
        """
        this is some description for our add_player method
        :param req:
        :return:
        """
        try:
            player = self._players_service.add_player(req)
        except PlayerAlreadyExists as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e
        return player.to_dto()
