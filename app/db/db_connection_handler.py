import logging
from contextlib import contextmanager
from typing import Any, Iterator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.db.db_models.base import Base

logger = logging.getLogger(__name__)


class DBConnectionHandler:
    def __init__(self, connection_string: str = "sqlite:///:memory:", **kwargs: Any) -> None:
        self._engine = create_engine(connection_string, echo=False, **kwargs)
        logger.info(f"Connected to database: {connection_string}")
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=False)

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        with self._engine.connect().execution_options() as connection:
            session = self._session_maker(bind=connection)
            try:
                yield session
            except Exception as e:
                session.rollback()
                logger.error(f"Error occurred in session scope: {e}")
                raise
            finally:
                session.close()

    def _create_all(self):
        Base.metadata.create_all(self._engine)

    def _drop_all(self):
        Base.metadata.drop_all(bind=self._engine)

    def get_engine(self) -> Engine:
        return self._engine
