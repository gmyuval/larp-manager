from typing import Optional

from app.db.daos.games_dao import GamesDAO
from app.db.db_connection_handler import DBConnectionHandler
from app.models.domain import Game
from app.models.dto.games_dto import GameCreateDTO


class GamesService:
    def __init__(self, db_handler: DBConnectionHandler):
        self._games_dao = GamesDAO(db_handler)

    def add_game(self, game_create_dto: GameCreateDTO) -> Optional[Game]:
        description = game_create_dto.description if game_create_dto.description else ""
        added_game = self._games_dao.add(
            name=game_create_dto.name,
            description=description,
            game_date=game_create_dto.game_start_date,
            registration_constraints={},
            registration_open_date=game_create_dto.registration_open_date,
            registration_close_date=game_create_dto.registration_close_date,
            overwrite_existing=False,
        )
        return Game.from_db_model(added_game)
