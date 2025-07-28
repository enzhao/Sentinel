import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.models import PortfolioDB
import uuid

# A sample decoded token to be returned by the mock auth verifier
SAMPLE_USER = {"uid": "test-user-init-123", "email": "test-init@example.com"}

@pytest.fixture(autouse=True)
def mock_auth():
    """
    Automatically mock the Firebase auth verification for all tests in this file.
    """
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER) as _mock:
        yield _mock

def test_initialize_user_creates_portfolio(test_client: TestClient):
    """
    Happy Path: Tests that the first call to /initialize creates a new portfolio.
    """
    # Mock the portfolio service to simulate that no portfolios exist yet
    with patch('src.services.portfolio_service.portfolio_service.get_portfolios_by_user', return_value=[]):
        with patch('src.services.portfolio_service.portfolio_service.create_portfolio') as mock_create:
            # Define a realistic portfolio object that should be "created"
            created_portfolio = PortfolioDB(
                name="My First Portfolio",
                userId=SAMPLE_USER["uid"]
            )
            mock_create.return_value = created_portfolio

            response = test_client.post(
                "/api/users/initialize",
                headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
            )

            assert response.status_code == 200
            mock_create.assert_called_once() # Ensure create_portfolio was called
            data = response.json()
            assert data["name"] == "My First Portfolio"
            assert data["userId"] == SAMPLE_USER["uid"]

def test_initialize_user_is_idempotent(test_client: TestClient):
    """
    Happy Path: Tests that a second call to /initialize does not create another portfolio.
    """
    # Mock the service to simulate that a portfolio already exists
    existing_portfolio = PortfolioDB(
        name="Existing Portfolio",
        userId=SAMPLE_USER["uid"]
    )
    
    with patch('src.services.portfolio_service.portfolio_service.get_portfolios_by_user', return_value=[existing_portfolio]):
        with patch('src.services.portfolio_service.portfolio_service.create_portfolio') as mock_create:
            
            response = test_client.post(
                "/api/users/initialize",
                headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
            )

            assert response.status_code == 200
            mock_create.assert_not_called() # Ensure create_portfolio was NOT called
            data = response.json()
            assert data["name"] == "Existing Portfolio"

def test_initialize_user_missing_idempotency_key(test_client: TestClient):
    """
    Error Path: Tests that the request fails without an Idempotency-Key header.
    """
    response = test_client.post(
        "/api/users/initialize",
        headers={"Authorization": "Bearer test-token"} # Missing Idempotency-Key
    )
    assert response.status_code == 400 # As enforced by the middleware
    data = response.json()
    assert "Idempotency-Key header is required" in data["detail"]

def test_initialize_user_invalid_idempotency_key(test_client: TestClient):
    """
    Error Path: Tests that the request fails with an invalid Idempotency-Key header.
    """
    response = test_client.post(
        "/api/users/initialize",
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": "not-a-uuid"}
    )
    assert response.status_code == 422 # FastAPI validation error for incorrect format
