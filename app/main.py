import logging
import uvicorn

import app
from app.api.http_handler import HttpHandler

logger = logging.getLogger(__name__)
http_handler = HttpHandler()

if __name__ == "__main__":
    uvicorn.run(
        http_handler.app,
        host="0.0.0.0",
        port=5000,
        log_level="debug"
    )