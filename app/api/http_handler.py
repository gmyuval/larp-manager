import logging

from fastapi import FastAPI

from app import APP_NAME
from app.api.players_handler import PlayersController
from app.services.players_service import PlayersService

logger = logging.getLogger(__name__)


class HttpHandler:
    def __init__(self, players_service: PlayersService):
        self.player_controller = PlayersController(players_service=players_service)
        self.app = self._create_http_api()
        self.app.include_router(self.player_controller.router)

    @staticmethod
    def _create_http_api() -> FastAPI:
        app = FastAPI(app_name=APP_NAME)

        @app.get("/_health")
        def heartbeat() -> dict[str, str]:
            return {"status": "ok"}

        return app
