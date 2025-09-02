import pytest
from fastapi.testclient import TestClient
from firebase_admin import firestore
from uuid import uuid4, UUID
from datetime import datetime, timezone

# --- Fixtures ---

@pytest.fixture(scope="function")
def test_user(db_client: firestore.Client) -> dict:
    """Creates a user document in Firestore for testing and yields the user data."""
    user_id = f"integration-test-user-{uuid4()}"
    user_data = {
        "uid": user_id,
        "email": f"{user_id}@example.com",
        "username": "Integration Test User",
        "defaultPortfolioId": None,
        "subscriptionStatus": "FREE",
        "notificationPreferences": ["EMAIL"],
        "createdAt": datetime.now(timezone.utc),
        "modifiedAt": datetime.now(timezone.utc),
    }
    db_client.collection("users").document(user_id).set(user_data)
    yield user_data
    # Cleanup is handled by the clear_firestore_emulator fixture in conftest.py

@pytest.fixture(scope="function")
def auth_headers(test_user: dict) -> dict:
    """Provides authentication headers for the test_user."""
    # In our test environment, the token is just the user's UID.
    return {"Authorization": f"Bearer {test_user['uid']}"}

@pytest.fixture(scope="function")
def user_with_portfolio(db_client: firestore.Client, test_user: dict) -> dict:
    """Creates a portfolio for the test_user and returns a dict with user and portfolio data."""
    portfolio_id = uuid4()
    now = datetime.now(timezone.utc)
    portfolio_data = {
        "portfolioId": str(portfolio_id),
        "userId": test_user["uid"],
        "name": "Test Portfolio",
        "description": "A portfolio for testing",
        "defaultCurrency": "USD",
        "cashReserve": {"totalAmount": 1000.0, "warChestAmount": 200.0},
        "createdAt": now,
        "modifiedAt": now,
        "ruleSetId": None
    }
    db_client.collection("portfolios").document(str(portfolio_id)).set(portfolio_data)
    
    return {
        "user": test_user,
        "portfolio": portfolio_data
    }

# --- Tests ---

def test_create_portfolio_success(test_client: TestClient, auth_headers: dict):
    """
    Tests successful portfolio creation (P_I_1001).
    """
    # ARRANGE
    idempotency_key = str(uuid4())
    headers = {**auth_headers, "Idempotency-Key": idempotency_key}
    payload = {
        "name": "My New Portfolio",
        "description": "For speculative plays",
        "defaultCurrency": "EUR",
        "cashReserve": {"totalAmount": 5000, "warChestAmount": 1000}
    }

    # ACT
    response = test_client.post("/api/v1/users/me/portfolios", headers=headers, json=payload)

    # ASSERT
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My New Portfolio"
    assert data["defaultCurrency"] == "EUR"
    assert data["cashReserve"]["totalAmount"] == 5000
    assert "portfolioId" in data

def test_create_portfolio_conflict(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict):
    """
    Tests that creating a portfolio with a duplicate name fails (P_E_1103).
    """
    # ARRANGE
    idempotency_key = str(uuid4())
    headers = {**auth_headers, "Idempotency-Key": idempotency_key}
    payload = {
        "name": user_with_portfolio["portfolio"]["name"], # Use existing name
        "defaultCurrency": "USD",
        "cashReserve": {"totalAmount": 100, "warChestAmount": 10}
    }

    # ACT
    response = test_client.post("/api/v1/users/me/portfolios", headers=headers, json=payload)

    # ASSERT
    assert response.status_code == 409
    assert response.json()["detail"] == "A portfolio with the name 'Test Portfolio' already exists."

def test_create_portfolio_idempotency(test_client: TestClient, auth_headers: dict):
    """
    Tests that replaying a request with the same idempotency key returns the original response (P_I_1002).
    """
    # ARRANGE
    idempotency_key = str(uuid4())
    headers = {**auth_headers, "Idempotency-Key": idempotency_key}
    payload = {"name": "Idempotent Portfolio", "defaultCurrency": "GBP", "cashReserve": {"totalAmount": 100, "warChestAmount": 10}}

    # ACT
    response1 = test_client.post("/api/v1/users/me/portfolios", headers=headers, json=payload)
    response2 = test_client.post("/api/v1/users/me/portfolios", headers=headers, json=payload)

    # ASSERT
    assert response1.status_code == 201
    assert response2.status_code == 201 # Middleware returns the stored status
    assert response1.json() == response2.json() # The body should be identical
    
    # Check that only one portfolio was actually created
    list_response = test_client.get("/api/v1/users/me/portfolios", headers=auth_headers)
    portfolios = [p for p in list_response.json() if p['name'] == "Idempotent Portfolio"]
    assert len(portfolios) == 1

def test_list_portfolios_success(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict):
    """
    Tests successful retrieval of a user's portfolio list (P_I_2201).
    """
    # ACT
    response = test_client.get("/api/v1/users/me/portfolios", headers=auth_headers)

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    summary = data[0]
    assert summary["name"] == user_with_portfolio["portfolio"]["name"]
    assert summary["portfolioId"] == user_with_portfolio["portfolio"]["portfolioId"]
    # Per spec, currentValue is stubbed with cash reserve total amount for now
    assert summary["currentValue"] == user_with_portfolio["portfolio"]["cashReserve"]["totalAmount"]

def test_get_portfolio_by_id_success(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict):
    """
    Tests successful retrieval of a single portfolio by its ID (P_I_2001).
    """
    # ARRANGE
    portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]

    # ACT
    response = test_client.get(f"/api/v1/users/me/portfolios/{portfolio_id}", headers=auth_headers)

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["portfolioId"] == portfolio_id
    assert data["name"] == user_with_portfolio["portfolio"]["name"]

def test_get_portfolio_by_id_not_found(test_client: TestClient, auth_headers: dict):
    """
    Tests that requesting a non-existent portfolio ID returns 404 (P_E_2102).
    """
    # ARRANGE
    non_existent_id = uuid4()

    # ACT
    response = test_client.get(f"/api/v1/users/me/portfolios/{non_existent_id}", headers=auth_headers)

    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == f"Portfolio with ID {non_existent_id} not found."

def test_get_portfolio_by_id_forbidden(test_client: TestClient, db_client: firestore.Client, user_with_portfolio: dict):
    """
    Tests that a user cannot retrieve a portfolio belonging to another user (P_E_2101).
    """
    # ARRANGE
    # 1. The portfolio to be requested (owned by user_with_portfolio)
    target_portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]

    # 2. A different user who will try to access it
    attacker_id = f"attacker-user-{uuid4()}"
    db_client.collection("users").document(attacker_id).set({"uid": attacker_id, "email": "attacker@a.com"})
    attacker_headers = {"Authorization": f"Bearer {attacker_id}"}

    # ACT
    response = test_client.get(f"/api/v1/users/me/portfolios/{target_portfolio_id}", headers=attacker_headers)

    # ASSERT
    assert response.status_code == 403
    assert response.json()["detail"] == f"User is not authorized to access portfolio {target_portfolio_id}."

def test_get_portfolio_chart_data_success(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict):
    """
    Tests that the chart data endpoint returns an empty list as specified (P_I_2401).
    """
    # ARRANGE
    portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]

    # ACT
    response = test_client.get(f"/api/v1/users/me/portfolios/{portfolio_id}/chart-data?range=1y", headers=auth_headers)

    # ASSERT
    assert response.status_code == 200
    assert response.json() == []

def test_update_portfolio_success(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict):
    """
    Tests successful portfolio update (P_I_3001).
    """
    # ARRANGE
    portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]
    headers = {**auth_headers, "Idempotency-Key": str(uuid4())}
    payload = {
        "name": "Updated Portfolio Name",
        "description": "Updated description",
        "defaultCurrency": "GBP",
        "cashReserve": {"totalAmount": 9999.0, "warChestAmount": 888.0}
    }

    # ACT
    response = test_client.put(f"/api/v1/users/me/portfolios/{portfolio_id}", headers=headers, json=payload)

    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Portfolio Name"
    assert data["description"] == "Updated description"
    assert data["defaultCurrency"] == "GBP"
    assert data["cashReserve"]["totalAmount"] == 9999.0

def test_update_portfolio_name_conflict(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict, db_client: firestore.Client):
    """
    Tests that updating a portfolio to a name that already exists fails (P_E_1103).
    """
    # ARRANGE
    # 1. Create a second portfolio with a unique name
    user_id = user_with_portfolio["user"]["uid"]
    second_portfolio_id = uuid4()
    db_client.collection("portfolios").document(str(second_portfolio_id)).set({
        "portfolioId": str(second_portfolio_id), "userId": user_id, "name": "Second Portfolio",
        "defaultCurrency": "USD", "cashReserve": {"totalAmount": 1.0, "warChestAmount": 1.0},
        "createdAt": datetime.now(timezone.utc), "modifiedAt": datetime.now(timezone.utc),
        "ruleSetId": None
    })

    # 2. Try to update the first portfolio to have the same name as the second one
    target_portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]
    headers = {**auth_headers, "Idempotency-Key": str(uuid4())}
    payload = {
        "name": "Second Portfolio", # Conflicting name
        "defaultCurrency": user_with_portfolio["portfolio"]["defaultCurrency"],
        "cashReserve": user_with_portfolio["portfolio"]["cashReserve"]
    }

    # ACT
    response = test_client.put(f"/api/v1/users/me/portfolios/{target_portfolio_id}", headers=headers, json=payload)

    # ASSERT
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_update_portfolio_forbidden(test_client: TestClient, user_with_portfolio: dict, db_client: firestore.Client):
    """
    Tests that a user cannot update a portfolio belonging to another user (P_E_3101).
    """
    # ARRANGE
    target_portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]
    
    # Create an attacker user
    attacker_id = f"attacker-user-{uuid4()}"
    db_client.collection("users").document(attacker_id).set({"uid": attacker_id, "email": "attacker@a.com"})
    attacker_headers = {"Authorization": f"Bearer {attacker_id}", "Idempotency-Key": str(uuid4())}
    
    payload = {
        "name": "Attacker Was Here",
        "defaultCurrency": "USD",
        "cashReserve": {"totalAmount": 123.0, "warChestAmount": 45.0}
    }

    # ACT
    response = test_client.put(f"/api/v1/users/me/portfolios/{target_portfolio_id}", headers=attacker_headers, json=payload)

    # ASSERT
    assert response.status_code == 403

def test_delete_portfolio_success(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict, db_client: firestore.Client):
    """
    Tests successful portfolio deletion (P_I_4001).
    """
    # ARRANGE
    portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]
    headers = {**auth_headers, "Idempotency-Key": str(uuid4())}

    # ACT
    response = test_client.delete(f"/api/v1/users/me/portfolios/{portfolio_id}", headers=headers)

    # ASSERT
    assert response.status_code == 204
    # Verify the document is gone from Firestore
    doc = db_client.collection("portfolios").document(portfolio_id).get()
    assert not doc.exists

def test_delete_default_portfolio_reassigns_default(test_client: TestClient, auth_headers: dict, user_with_portfolio: dict, db_client: firestore.Client):
    """
    Tests that deleting the default portfolio automatically reassigns a new default (P_I_4003).
    """
    # ARRANGE
    # 1. Create a second portfolio
    user_id = user_with_portfolio["user"]["uid"]
    second_portfolio_id = uuid4()
    db_client.collection("portfolios").document(str(second_portfolio_id)).set({
        "portfolioId": str(second_portfolio_id), "userId": user_id, "name": "Second Portfolio",
        "defaultCurrency": "USD", "cashReserve": {"totalAmount": 1.0, "warChestAmount": 1.0},
        "createdAt": datetime.now(timezone.utc), "modifiedAt": datetime.now(timezone.utc),
        "ruleSetId": None
    })

    # 2. Set the first portfolio as the default
    default_portfolio_id = user_with_portfolio["portfolio"]["portfolioId"]
    db_client.collection("users").document(user_id).update({"defaultPortfolioId": default_portfolio_id})

    # 3. Delete the default portfolio
    headers = {**auth_headers, "Idempotency-Key": str(uuid4())}
    response = test_client.delete(f"/api/v1/users/me/portfolios/{default_portfolio_id}", headers=headers)

    # ASSERT
    assert response.status_code == 204
    # Verify the user's defaultPortfolioId has been updated to the second portfolio
    user_doc = db_client.collection("users").document(user_id).get()
    assert user_doc.to_dict()["defaultPortfolioId"] == str(second_portfolio_id)