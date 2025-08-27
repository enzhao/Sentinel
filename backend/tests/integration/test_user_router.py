import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from firebase_admin import auth, firestore
from datetime import datetime, timezone

# Import NotificationChannel from internal_models for consistency
from src.core.internal_models import NotificationChannel

# --- Test Constants ---
MOCK_USER_UID = "test-user-123"
MOCK_USER_EMAIL = "test-user@example.com"
MOCK_USER_PASSWORD = "strongpassword"

# --- Helper Functions ---
def create_auth_user_and_get_token(uid, email, password):
    """Creates a user in the Auth emulator."""
    try:
        auth.create_user(uid=uid, email=email, password=password)
    except auth.EmailAlreadyExistsError:
        pass

# --- Fixtures ---
@pytest.fixture(scope="function")
def test_user(test_client: TestClient, db_client: firestore.Client):
    """
    Creates a user in Auth and Firestore, yielding UID and auth header.
    """
    create_auth_user_and_get_token(MOCK_USER_UID, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)

    portfolio_id = str(uuid4())
    now = datetime.now(timezone.utc)
    
    # Added createdAt and modifiedAt to match the Pydantic User model.
    user_data = {
        "uid": MOCK_USER_UID,
        "username": "testuser",
        "email": MOCK_USER_EMAIL,
        "defaultPortfolioId": portfolio_id,
        "subscriptionStatus": "FREE",
        "notificationPreferences": [NotificationChannel.EMAIL.value],
        "createdAt": now,
        "modifiedAt": now,
    }
    db_client.collection("users").document(MOCK_USER_UID).set(user_data)
    
    portfolio_data = {
        "portfolioId": portfolio_id,
        "userId": MOCK_USER_UID,
        "name": "My First Portfolio",
        "description": "Test portfolio",
        "defaultCurrency": "EUR",
        "cashReserve": {"totalAmount": 0.0, "warChestAmount": 0.0},
        "ruleSetId": None,
        "createdAt": now,
        "modifiedAt": now,
    }
    db_client.collection("portfolios").document(portfolio_id).set(portfolio_data)

    auth_header = {"Authorization": f"Bearer {MOCK_USER_UID}"}
    
    yield MOCK_USER_UID, auth_header

    # Teardown
    try:
        auth.delete_user(MOCK_USER_UID)
    except auth.UserNotFoundError:
        pass

# --- Test Cases ---
# (The rest of your test cases remain the same)

def test_get_user_settings_success(test_client: TestClient, test_user):
    """Test successful retrieval of user settings."""
    user_uid, auth_header = test_user
    response = test_client.get("/api/v1/users/me/settings", headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == user_uid
    assert data["email"] == MOCK_USER_EMAIL
    assert data["notificationPreferences"] == [NotificationChannel.EMAIL.value]

def test_get_user_settings_not_found(test_client: TestClient, test_user, db_client: firestore.Client):
    """Test retrieval when Firestore document is missing."""
    user_uid, auth_header = test_user
    db_client.collection("users").document(user_uid).delete()
    
    response = test_client.get("/api/v1/users/me/settings", headers=auth_header)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User settings not found."}

def test_update_user_settings_success(test_client: TestClient, test_user, db_client: firestore.Client):
    """Test successful update of user settings."""
    user_uid, auth_header = test_user
    new_portfolio_id = str(uuid4())
    db_client.collection("portfolios").document(new_portfolio_id).set({
        "portfolioId": new_portfolio_id,
        "userId": user_uid,
        "name": "My New Portfolio",
        "description": "New test portfolio",
        "defaultCurrency": "EUR",
        "cashReserve": {"totalAmount": 0.0, "warChestAmount": 0.0},
        "ruleSetId": None,
        "createdAt": datetime.now(timezone.utc),
        "modifiedAt": datetime.now(timezone.utc),
    })

    request_payload = {
        "defaultPortfolioId": new_portfolio_id,
        "notificationPreferences": [NotificationChannel.PUSH.value, NotificationChannel.EMAIL.value]
    }
    
    response = test_client.put(
        "/api/v1/users/me/settings", 
        headers={**auth_header, "Idempotency-Key": str(uuid4())}, 
        json=request_payload
    )
    
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["defaultPortfolioId"] == new_portfolio_id
    assert updated_data["notificationPreferences"] == [NotificationChannel.PUSH.value, NotificationChannel.EMAIL.value]
    
    doc = db_client.collection("users").document(user_uid).get()
    assert doc.to_dict()["defaultPortfolioId"] == new_portfolio_id
    assert doc.to_dict()["notificationPreferences"] == [NotificationChannel.PUSH.value, NotificationChannel.EMAIL.value]

def test_update_user_settings_invalid_portfolio(test_client: TestClient, test_user):
    """Test update with a portfolio ID that doesn't exist."""
    user_uid, auth_header = test_user
    invalid_portfolio_id = str(uuid4())
    request_payload = { "defaultPortfolioId": invalid_portfolio_id }
    
    response = test_client.put(
        "/api/v1/users/me/settings", 
        headers={**auth_header, "Idempotency-Key": str(uuid4())}, 
        json=request_payload
    )
    
    assert response.status_code == 403

def test_logout_user_success(test_client: TestClient, test_user):
    """Test successful logout of a user."""
    user_uid, auth_header = test_user
    response = test_client.post(
        "/api/v1/auth/logout", 
        headers={**auth_header, "Idempotency-Key": str(uuid4())}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "U_I_4001: User logged out successfully."
    
    