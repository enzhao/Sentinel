import pytest
from uuid import uuid4, UUID
from datetime import datetime, timezone
from firebase_admin import firestore
from collections import Counter

# Import the services and models we are going to test
from src.services.user_service import UserService
from src.services.portfolio_service import PortfolioService
from src.core.internal_models import UserDB, NotificationChannel

# --- Fixtures for Service-Level Testing ---

@pytest.fixture(scope="module")
def portfolio_service(db_client: firestore.Client) -> PortfolioService:
    """Provides an instance of the PortfolioService for use in tests."""
    return PortfolioService(db_client)

@pytest.fixture(scope="module")
def user_service(db_client: firestore.Client, portfolio_service: PortfolioService) -> UserService:
    """Provides an instance of the UserService for testing."""
    return UserService(db_client, portfolio_service)

@pytest.fixture(scope="function")
def created_user(db_client: firestore.Client) -> dict:
    """
    A fixture that creates a user and a default portfolio directly in the
    emulator database, then……

    yields the user's data.
    Cleans up after the test.
    """
    user_id = f"service-test-user-{uuid4()}"
    portfolio_id = uuid4()
    now = datetime.now(timezone.utc)

    user_data = {
        "uid": user_id,
        "email": f"{user_id}@example.com",
        "username": "Service Test User",
        "defaultPortfolioId": str(portfolio_id),
        "subscriptionStatus": "FREE",
        "notificationPreferences": [NotificationChannel.EMAIL.value],  # Store string value
        "createdAt": now,
        "modifiedAt": now,
    }
    db_client.collection("users").document(user_id).set(user_data)

    portfolio_data = {
        "portfolioId": str(portfolio_id),
        "userId": user_id,
        "name": "Default Portfolio",
    }
    db_client.collection("portfolios").document(str(portfolio_id)).set(portfolio_data)

    yield user_data

    # Teardown - the conftest clear_firestore_emulator fixture handles this automatically
    # but it's good practice to be explicit if needed.
    # db_client.collection("users").document(user_id).delete()
    # db_client.collection("portfolios").document(str(portfolio_id)).delete()


# --- Unit Tests for UserService ---

def test_get_user_by_uid_success(user_service: UserService, created_user: dict):
    """
    Tests that a user can be successfully retrieved by their UID.
    """
    # ARRANGE: The `created_user` fixture has already created the user.
    user_id = created_user["uid"]

    # ACT: Call the service method directly.
    retrieved_user = user_service.get_user_by_uid(user_id)

    # ASSERT: Check that the returned object is correct.
    assert retrieved_user is not None
    assert isinstance(retrieved_user, UserDB)
    assert retrieved_user.uid == user_id
    assert retrieved_user.email == created_user["email"]

def test_get_user_by_uid_not_found(user_service: UserService):
    """
    Tests that get_user_by_uid returns None for a non-existent user.
    """
    # ARRANGE: A non-existent user ID.
    non_existent_uid = "i-do-not-exist"

    # ACT: Call the service method.
    retrieved_user = user_service.get_user_by_uid(non_existent_uid)

    # ASSERT: Check that the result is None.
    assert retrieved_user is None

def test_update_user_settings_success(user_service: UserService, db_client: firestore.Client, created_user: dict):
    """
    Tests that user settings can be successfully updated.
    """
    # ARRANGE:
    # 1. Get the UID of the user created by the fixture.
    user_id = created_user["uid"]
    
    # 2. Create a second, new portfolio for this user to switch to.
    new_portfolio_id = uuid4()
    db_client.collection("portfolios").document(str(new_portfolio_id)).set({
        "portfolioId": str(new_portfolio_id),
        "userId": user_id,
        "name": "New Portfolio",
    })

    # 3. Define the update payload using the Enum objects.
    update_data = {
        "defaultPortfolioId": new_portfolio_id,
        "notificationPreferences": [NotificationChannel.EMAIL, NotificationChannel.PUSH]
    }

    # ACT: Call the service method to update the user.
    updated_user = user_service.update_user_settings(user_id, update_data)

    # ASSERT:
    # 1. Check the returned UserDB object.
    assert updated_user.defaultPortfolioId == new_portfolio_id
    
    # Compare notificationPreferences as strings
    actual_preferences = [pref.value for pref in updated_user.notificationPreferences]
    expected_preferences = [NotificationChannel.EMAIL.value, NotificationChannel.PUSH.value]
    assert Counter(actual_preferences) == Counter(expected_preferences)
    
    # 2. Directly check the database to be 100% sure the data was written correctly.
    user_doc = db_client.collection("users").document(user_id).get()
    assert user_doc.to_dict()["defaultPortfolioId"] == str(new_portfolio_id)
    assert user_doc.to_dict()["modifiedAt"] > created_user["modifiedAt"]

def test_update_user_settings_invalid_portfolio(user_service: UserService, created_user: dict):
    """
    Tests that the service raises a ValueError if the user tries to set a
    default portfolio that does not exist.
    """
    # ARRANGE:
    user_id = created_user["uid"]
    non_existent_portfolio_id = uuid4()
    update_data = {"defaultPortfolioId": non_existent_portfolio_id}

    # ACT & ASSERT: Use pytest.raises to confirm that the expected exception is thrown.
    with pytest.raises(ValueError, match="Invalid default portfolio specified"):
        user_service.update_user_settings(user_id, update_data)
        
        