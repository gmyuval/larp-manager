from app.db.db_connection_handler import DBConnectionHandler


class BaseDAO:
    def __init__(self, db_handler: DBConnectionHandler):
        self._db_handler = db_handler
