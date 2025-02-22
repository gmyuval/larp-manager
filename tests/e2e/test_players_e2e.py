import pytest

from uuid import UUID
from fastapi.testclient import TestClient

from tests.e2e.conftest import TestEnvironment


class TestPlayersAPI:
    @pytest.fixture
    def valid_player_data(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "date_of_birth": "1990-01-01",
        }

    @pytest.fixture
    def another_player_data(self):
        return {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone_number": "+0987654321",
            "date_of_birth": "1992-02-02",
        }

    def test_health_check(self, env: TestEnvironment):
        response = env.client.get("/_health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_add_player_success(self, env: TestEnvironment, valid_player_data):
        """Test successful player creation"""
        response = env.client.post("/players/add_player", json=valid_player_data)
        assert response.status_code == 200

        player = response.json()
        assert player["first_name"] == valid_player_data["first_name"]
        assert player["last_name"] == valid_player_data["last_name"]
        assert player["email"] == valid_player_data["email"]
        assert player["phone_number"] == valid_player_data["phone_number"]
        assert "id" in player
        # Verify UUID is valid
        UUID(player["id"])

    def test_add_player_duplicate_email(self, env: TestEnvironment, valid_player_data):
        """Test handling of duplicate email addresses"""
        # Create first player
        response = env.client.post("/players/add_player", json=valid_player_data)
        assert response.status_code == 200

        # Try to create another player with same email
        duplicate_data = valid_player_data.copy()
        duplicate_data["phone_number"] = "+1111111111"  # different phone
        response = env.client.post("/players/add_player", json=duplicate_data)

        # Expect status code 409 on the response
        assert response.status_code == 409
        detail = response.json()["detail"]
        assert (
            detail
            == f"Player with name {duplicate_data["first_name"]} {duplicate_data["last_name"]} and email {duplicate_data["email"]} already exists"
        )

    def test_get_player_by_id(self, env: TestEnvironment, valid_player_data):
        """Test retrieving a player by ID"""
        # First create a player
        create_response = env.client.post("/players/add_player", json=valid_player_data)
        assert create_response.status_code == 200
        player_id = create_response.json()["id"]

        # Then retrieve the player
        response = env.client.get(f"/players/{player_id}")
        assert response.status_code == 200
        player = response.json()
        assert player["id"] == player_id
        assert player["first_name"] == valid_player_data["first_name"]
        assert player["email"] == valid_player_data["email"]

    def test_get_player_invalid_id(self, env: TestEnvironment):
        """Test handling of invalid player IDs"""
        response = env.client.get("/players/invalid-uuid")
        assert response.status_code == 400

    def test_get_player_nonexistent_id(self, env: TestEnvironment):
        """Test handling of non-existent player IDs"""
        response = env.client.get("/players/12345678-1234-5678-1234-567812345678")
        assert response.status_code == 404

    def test_get_players_by_criteria_single_field(self, env: TestEnvironment, valid_player_data):
        """Test filtering players by a single criterion"""
        # Create a player first
        create_response = env.client.post("/players/add_player", json=valid_player_data)
        assert create_response.status_code == 200

        # Search by first name
        response = env.client.post("/players/by_criteria", json={"first_name": valid_player_data["first_name"]})
        assert response.status_code == 200
        players = response.json()
        assert len(players) == 1
        assert players[0]["first_name"] == valid_player_data["first_name"]

    def test_get_players_by_criteria_multiple_fields(self, env: TestEnvironment, valid_player_data, another_player_data):
        """Test filtering players by multiple criteria"""
        # Create two players
        env.client.post("/players/add_player", json=valid_player_data)
        env.client.post("/players/add_player", json=another_player_data)

        # Search by first name and last name
        response = env.client.post(
            "/players/by_criteria", json={"first_name": valid_player_data["first_name"], "last_name": valid_player_data["last_name"]}
        )
        assert response.status_code == 200
        players = response.json()
        assert len(players) == 1
        assert players[0]["first_name"] == valid_player_data["first_name"]
        assert players[0]["last_name"] == valid_player_data["last_name"]

    def test_get_players_by_criteria_no_results(self, env: TestEnvironment):
        """Test search with criteria that match no players"""
        response = env.client.post("/players/by_criteria", json={"first_name": "NonexistentName"})
        assert response.status_code == 200
        players = response.json()
        assert len(players) == 0

    def test_get_players_by_criteria_with_limit(self, env: TestEnvironment, valid_player_data, another_player_data):
        """Test limiting the number of results"""
        # Create two players
        env.client.post("/players/add_player", json=valid_player_data)
        env.client.post("/players/add_player", json=another_player_data)

        # Get players with limit=1
        response = env.client.post("/players/by_criteria", json={"limit": 1})
        assert response.status_code == 200
        players = response.json()
        assert len(players) == 1

    def test_get_players_empty_criteria(self, env: TestEnvironment):
        """Test handling of empty search criteria"""
        response = env.client.post("/players/by_criteria", json={})
        assert response.status_code == 422  # Validation error

    def test_add_player_invalid_data(self, env: TestEnvironment):
        """Test handling of invalid player data"""
        invalid_data = {
            "first_name": "",  # Empty name
            "last_name": "Doe",
            "email": "invalid-email",  # Invalid email format
            "phone_number": "123",  # Invalid phone format
        }
        response = env.client.post("/players/add_player", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_add_player_missing_required_fields(self, env: TestEnvironment):
        """Test handling of missing required fields"""
        incomplete_data = {
            "first_name": "John"
            # Missing last_name and email
        }
        response = env.client.post("/players/add_player", json=incomplete_data)
        assert response.status_code == 422  # Validation error

    def test_get_players_by_criteria_case_sensitivity(self, env: TestEnvironment, valid_player_data):
        """Test case sensitivity in search criteria"""
        # Create a player
        env.client.post("/players/add_player", json=valid_player_data)

        # Search with different case
        response = env.client.post("/players/by_criteria", json={"first_name": valid_player_data["first_name"].upper()})
        assert response.status_code == 200
        players = response.json()
        # The behavior here depends on your implementation:
        # If case-sensitive, length should be 0
        # If case-insensitive, length should be 1
        if len(players) > 0:
            assert players[0]["first_name"] == valid_player_data["first_name"]
