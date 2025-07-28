import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid
from datetime import datetime

# A sample decoded token to be returned by the mock auth verifier
SAMPLE_USER = {"uid": "test-user-123", "email": "test@example.com"}

@pytest.fixture(autouse=True)
def mock_auth():
    """
    Automatically mock the Firebase auth verification for all tests in this file.
    """
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER) as _mock:
        yield _mock

def seed_market_data(ticker: str, price: float):
    """Helper function to seed market data in our mock DB."""
    from src.firebase_setup import db
    from src.models import MarketDataDB

    today_str = datetime.now().strftime('%Y-%m-%d')
    market_data = MarketDataDB(
        ticker=ticker,
        open=price, high=price, low=price, close=price, volume=100000
    )
    db.collection('marketData').document(ticker).collection('dailyPrices').document(today_str).set(market_data.model_dump())

def test_create_and_get_enriched_portfolio(test_client: TestClient):
    """
    Tests creating a portfolio, adding a holding, and then retrieving it to
    ensure it is correctly enriched with market data. This is a full
    end-to-end integration test using the mock database.
    """
    # 1. Seed the database with market data for the ticker we will use
    seed_market_data("AAPL", 200.0)

    # 2. Create an empty portfolio
    portfolio_name = "My Enriched Portfolio"
    create_response = test_client.post(
        "/api/portfolios",
        json={"name": portfolio_name},
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
    )
    assert create_response.status_code == 201
    portfolio_id = create_response.json()["portfolioId"]

    # 3. Add a holding to that portfolio
    add_holding_response = test_client.post(
        f"/api/portfolios/{portfolio_id}/holdings",
        json={
            "ticker": "AAPL",
            "lots": [{"purchaseDate": "2025-01-01T12:00:00Z", "quantity": 10, "purchasePrice": 150.0}]
        },
        headers={"Authorization": "Bearer test-token", "Idempotency-Key": str(uuid.uuid4())}
    )
    assert add_holding_response.status_code == 200

    # 4. Retrieve the final, updated portfolio
    get_response = test_client.get(
        f"/api/portfolios/{portfolio_id}",
        headers={"Authorization": "Bearer test-token"}
    )
    assert get_response.status_code == 200
    data = get_response.json()
    
    # 5. Assert that the final state is correct and enriched
    assert data["name"] == portfolio_name
    assert len(data["holdings"]) == 1
    assert data["holdings"][0]["ticker"] == "AAPL"
    assert data["totalCost"] == 1500.0  # 10 * 150
    assert data["currentValue"] == 2000.0 # 10 * 200 (from seeded market data)
    assert data["preTaxGainLoss"] == 500.0

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