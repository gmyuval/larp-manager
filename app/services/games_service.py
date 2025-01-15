from app.db.daos.games_dao import GamesDAO
from app.db.db_connection_handler import DBConnectionHandler
from app.domain.game import Game


class GamesService:
    def __init__(self, db_handler: DBConnectionHandler):
        self._games_dao = GamesDAO(db_handler)

    def add_game(self, game: Game):
        pass
