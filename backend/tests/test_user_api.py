import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.models import UserDB, PortfolioDB, UpdateUserSettingsRequest
import uuid

# A sample decoded token to be returned by the mock auth verifier
SAMPLE_USER_AUTH = {"uid": "test-user-api-123", "email": "test-api@example.com"}

@pytest.fixture(autouse=True)
def mock_auth():
    """
    Automatically mock the Firebase auth verification for all tests in this file.
    """
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_AUTH) as _mock:
        yield _mock

def test_initialize_user_happy_path(test_client: TestClient):
    """
    Tests that the first call to /initialize creates a new user and a default portfolio,
    and correctly links them.
    """
    # Mock services to simulate a new user
    with patch('src.services.user_service.user_service.get_user', return_value=None):
        with patch('src.services.user_service.user_service.create_user') as mock_create_user:
            with patch('src.services.portfolio_service.portfolio_service.create_portfolio') as mock_create_portfolio:
                with patch('src.services.user_service.user_service.update_user_settings') as mock_update_user:

                    # Define what the mocks should return
                    created_user = UserDB(uid=SAMPLE_USER_AUTH["uid"], email=SAMPLE_USER_AUTH["email"], username="test-api")
                    created_portfolio = PortfolioDB(portfolioId="pf-default-123", userId=SAMPLE_USER_AUTH["uid"], name="My First Portfolio")
                    
                    # Create final user object by updating the defaultPortfolioId
                    user_data = created_user.model_dump()
                    user_data['defaultPortfolioId'] = created_portfolio.portfolioId
                    final_user = UserDB(**user_data)

                    mock_create_user.return_value = created_user
                    mock_create_portfolio.return_value = created_portfolio
                    mock_update_user.return_value = final_user

                    response = test_client.post(
                        "/api/users/initialize",
                        headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
                    )

                    assert response.status_code == 201
                    mock_create_user.assert_called_once()
                    mock_create_portfolio.assert_called_once()
                    mock_update_user.assert_called_once()
                    
                    data = response.json()
                    assert data["uid"] == SAMPLE_USER_AUTH["uid"]
                    assert data["defaultPortfolioId"] == "pf-default-123"

def test_initialize_user_already_exists(test_client: TestClient):
    """
    Tests that if a user already exists, /initialize returns the existing user data
    without creating a new user or portfolio.
    """
    existing_user = UserDB(uid=SAMPLE_USER_AUTH["uid"], email=SAMPLE_USER_AUTH["email"], username="existing_user", defaultPortfolioId="pf-existing-123")
    
    with patch('src.services.user_service.user_service.get_user', return_value=existing_user):
        with patch('src.services.user_service.user_service.create_user') as mock_create_user:
            response = test_client.post(
                "/api/users/initialize",
                headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
            )
            assert response.status_code == 201 # The endpoint returns the user if exists
            mock_create_user.assert_not_called()
            data = response.json()
            assert data["username"] == "existing_user"

def test_get_user_me(test_client: TestClient):
    """
    Tests the GET /me endpoint.
    """
    user_data = UserDB(uid=SAMPLE_USER_AUTH["uid"], email=SAMPLE_USER_AUTH["email"], username="test_user")
    with patch('src.services.user_service.user_service.get_user', return_value=user_data):
        response = test_client.get("/api/users/me", headers={"Authorization": "Bearer test-token"})
        assert response.status_code == 200
        data = response.json()
        assert data["uid"] == SAMPLE_USER_AUTH["uid"]

def test_update_user_settings(test_client: TestClient):
    """
    Tests the PUT /me/settings endpoint.
    """
    updated_user_data = UserDB(uid=SAMPLE_USER_AUTH["uid"], email=SAMPLE_USER_AUTH["email"], username="new_username", defaultPortfolioId="new-pf-id")
    
    with patch('src.services.user_service.user_service.update_user_settings', return_value=updated_user_data) as mock_update:
        update_payload = {"username": "new_username", "defaultPortfolioId": "new-pf-id"}
        response = test_client.put(
            "/api/users/me/settings",
            json=update_payload,
            headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
        )
        assert response.status_code == 200
        mock_update.assert_called_once()
        data = response.json()
        assert data["username"] == "new_username"
        assert data["defaultPortfolioId"] == "new-pf-id"

def test_update_user_settings_invalid_portfolio_id(test_client: TestClient):
    """
    Tests that the API returns a 400 if the user tries to set a default portfolio they don't own.
    """
    with patch('src.services.user_service.user_service.update_user_settings', side_effect=ValueError("Invalid defaultPortfolioId")):
        update_payload = {"defaultPortfolioId": "foreign-portfolio-id"}
        response = test_client.put(
            "/api/users/me/settings",
            json=update_payload,
            headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
        )
        assert response.status_code == 400
        assert "Invalid defaultPortfolioId" in response.json()["detail"]

def test_get_user_portfolios(test_client: TestClient):
    """
    Tests the GET /me/portfolios endpoint.
    """
    portfolios_data = [
        PortfolioDB(portfolioId="pf1", userId=SAMPLE_USER_AUTH["uid"], name="Portfolio 1"),
        PortfolioDB(portfolioId="pf2", userId=SAMPLE_USER_AUTH["uid"], name="Portfolio 2")
    ]
    with patch('src.services.portfolio_service.portfolio_service.get_portfolios_by_user', return_value=portfolios_data):
        response = test_client.get("/api/users/me/portfolios", headers={"Authorization": "Bearer test-token"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Portfolio 1"
        assert data[1]["name"] == "Portfolio 2"
