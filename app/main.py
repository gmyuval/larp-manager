import logging

import uvicorn

# import app
from app.api.http_handler import HttpHandler
from app.db.db_connection_handler import DBConnectionHandler
from app.services.players_service import PlayersService

logger = logging.getLogger(__name__)
db_handler = DBConnectionHandler()
players_service = PlayersService(db_handler)
http_handler = HttpHandler(players_service=players_service)

if __name__ == "__main__":
    uvicorn.run(http_handler.app, host="0.0.0.0", port=5000, log_level="debug")
