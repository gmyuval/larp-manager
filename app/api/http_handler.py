import logging
from fastapi import FastAPI

from app import APP_NAME
from app.api.players_handler import PlayersController

logger = logging.getLogger(__name__)


class HttpHandler:
    def __init__(self):
        self.player_controller = PlayersController()
        self.app = self._create_http_api()
        self.app.include_router(self.player_controller.router)

    def _create_http_api(self):
        app = FastAPI(app_name=APP_NAME)

        @app.get("/_health")
        def heartbeat() -> dict[str, str]:
            return {"status": "ok"}

        return app


