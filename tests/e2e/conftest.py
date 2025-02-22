import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool

from app.api.http_handler import HttpHandler
from app.db.db_connection_handler import DBConnectionHandler
from app.db.db_models.base import Base
from app.services.players_service import PlayersService


class TestEnvironment:
    DEFAULT_DB_URL = "sqlite:///:memory:"

    def __init__(self, db_url: str = DEFAULT_DB_URL):
        self.db_handler = DBConnectionHandler(connection_string=db_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)
        self._engine = self.db_handler.get_engine()

        self.db_handler._create_all()

        self.player_service = PlayersService(self.db_handler)
        self.http_handler = HttpHandler(players_service=self.player_service)
        self.client = TestClient(self.http_handler.app)

    @staticmethod
    def get_new_player_payload() -> dict[str, str]:
        """Returns a sample payload for creating a new player."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "date_of_birth": "1990-01-01",
        }

    @staticmethod
    def get_player_criteria() -> dict[str, str]:
        """Returns sample criteria for filtering players."""
        return {"first_name": "John"}


@pytest.fixture(scope="session")
def env():
    """Provides an instance of TestEnvironment to the tests."""
    environment = TestEnvironment()
    yield environment
    # Optional teardown logic—for example, drop all tables:
    Base.metadata.drop_all(bind=environment.db_handler.get_engine())


#
# @pytest.fixture
# def test_client():
#     """Create a test client with a fresh database"""
#     db_handler = DBConnectionHandler(connection_string=TestEnvironment.DEFAULT_DB_URL, pool_size=10, pool_pre_ping=True)
#     players_service = PlayersService(db_handler)
#     http_handler = HttpHandler(players_service=players_service, debug=True)
#
#     with TestClient(http_handler.app) as client:
#         yield client
#
#
# @pytest.fixture
# def test_data():
#     """Provide common test data"""
#     return {
#         "sample_player": {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone_number": "+1234567890"},
#         "sample_players": [
#             {"first_name": "Alice", "last_name": "Smith", "email": "alice.smith@example.com"},
#             {"first_name": "Bob", "last_name": "Jones", "email": "bob.jones@example.com"},
#         ],
#     }
