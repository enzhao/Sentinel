import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid

# A sample decoded token to be returned by the mock auth verifier
SAMPLE_USER = {"uid": "test-user-123", "email": "test@example.com"}

@pytest.fixture(autouse=True)
def mock_auth():
    """
    Automatically mock the Firebase auth verification for all tests in this file.
    """
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER) as _mock:
        yield _mock

def test_create_and_get_portfolio(test_client: TestClient):
    """
    Tests creating a new portfolio and then retrieving it.
    """
    # 1. Create a portfolio
    response = test_client.post(
        "/api/portfolios",
        json={"name": "My Test Portfolio"},
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
    )
    assert response.status_code == 201
    created_data = response.json()
    assert created_data["name"] == "My Test Portfolio"
    assert created_data["userId"] == SAMPLE_USER["uid"]
    portfolio_id = created_data["portfolioId"]

    # 2. Retrieve the portfolio
    response = test_client.get(
        f"/api/portfolios/{portfolio_id}",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    retrieved_data = response.json()
    assert retrieved_data["name"] == "My Test Portfolio"
    assert retrieved_data["portfolioId"] == portfolio_id

def test_idempotency_for_create(test_client: TestClient):
    """
    Tests that creating a portfolio is idempotent.
    """
    key = str(uuid.uuid4())
    # 1. First request to create
    response1 = test_client.post(
        "/api/portfolios",
        json={"name": "Idempotent Test"},
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": key}
    )
    assert response1.status_code == 201
    data1 = response1.json()

    # 2. Second request with the same key
    response2 = test_client.post(
        "/api/portfolios",
        json={"name": "Idempotent Test"},
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": key}
    )
    # It should return the same response without creating a new portfolio
    assert response2.status_code == 201
    data2 = response2.json()
    assert data1["portfolioId"] == data2["portfolioId"]

def test_unauthorized_access(test_client: TestClient):
    """
    Tests that unauthorized access is blocked.
    """
    response = test_client.get("/api/portfolios")
    # The middleware should block this, but if not, the dependency will
    assert response.status_code in [401, 403]
