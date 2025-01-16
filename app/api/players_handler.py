import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.dto.player_dto import PlayerCreateDTO, PlayerDTO
from app.exceptions import PlayerAlreadyExists
from app.services.players_service import PlayersService

logger = logging.getLogger(__name__)


class PlayersController:
    router = APIRouter(prefix="/players")

    def __init__(self, players_service: PlayersService):
        self._players_service = players_service

    @router.get("/get_player/{player_id}")
    def get_player(self, player_id: str) -> Optional[PlayerDTO]:
        return None

    @router.post("/add_player", response_model=PlayerDTO)
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
