import pytest
from unittest.mock import patch, MagicMock
from src.services.user_service import UserService, users_collection
from src.models import UserDB, UpdateUserSettingsRequest

SAMPLE_UID = "test-user-123"
SAMPLE_EMAIL = "test@example.com"

def test_create_user():
    """
    Tests that a user document is correctly created in Firestore.
    """
    with patch.object(users_collection, 'document') as mock_document:
        mock_doc_ref = MagicMock()
        mock_document.return_value = mock_doc_ref

        user = UserService.create_user(uid=SAMPLE_UID, email=SAMPLE_EMAIL, username="testuser")

        mock_document.assert_called_with(SAMPLE_UID)
        mock_doc_ref.set.assert_called_once()
        
        # Check the data that was passed to set()
        call_args = mock_doc_ref.set.call_args[0][0]
        assert call_args['uid'] == SAMPLE_UID
        assert call_args['email'] == SAMPLE_EMAIL
        assert call_args['username'] == "testuser"

def test_get_user_exists():
    """
    Tests retrieving an existing user.
    """
    mock_user_data = {"uid": SAMPLE_UID, "email": SAMPLE_EMAIL, "username": "testuser"}
    
    with patch.object(users_collection, 'document') as mock_document:
        mock_doc_ref = MagicMock()
        mock_doc_ref.get.return_value.exists = True
        mock_doc_ref.get.return_value.to_dict.return_value = mock_user_data
        mock_document.return_value = mock_doc_ref

        user = UserService.get_user(SAMPLE_UID)

        assert user is not None
        assert user.uid == SAMPLE_UID
        assert user.email == SAMPLE_EMAIL

def test_get_user_not_exists():
    """
    Tests retrieving a non-existent user.
    """
    with patch.object(users_collection, 'document') as mock_document:
        mock_doc_ref = MagicMock()
        mock_doc_ref.get.return_value.exists = False
        mock_document.return_value = mock_doc_ref

        user = UserService.get_user("non-existent-uid")
        assert user is None

def test_update_user_settings():
    """
    Tests updating a user's settings.
    """
    # Mock get_user to return a user
    with patch.object(UserService, 'get_user', return_value=UserDB(uid=SAMPLE_UID, email=SAMPLE_EMAIL, username="old_name")):
        # Mock get_portfolio_by_id to simulate portfolio ownership validation
        with patch('src.services.portfolio_service.portfolio_service.get_portfolio_by_id', return_value=MagicMock()):
             with patch.object(users_collection, 'document') as mock_document:
                mock_doc_ref = MagicMock()
                mock_document.return_value = mock_doc_ref

                update_request = UpdateUserSettingsRequest(username="new_name", defaultPortfolioId="pf-123")
                UserService.update_user_settings(SAMPLE_UID, update_request)

                mock_document.assert_called_with(SAMPLE_UID)
                mock_doc_ref.update.assert_called_once_with({"username": "new_name", "defaultPortfolioId": "pf-123"})

def test_update_user_settings_invalid_portfolio():
    """
    Tests that updating with an invalid defaultPortfolioId raises a ValueError.
    """
    with patch.object(UserService, 'get_user', return_value=UserDB(uid=SAMPLE_UID, email=SAMPLE_EMAIL, username="testuser")):
        # Simulate portfolio not being found
        with patch('src.services.portfolio_service.portfolio_service.get_portfolio_by_id', return_value=None):
            with pytest.raises(ValueError, match="Invalid defaultPortfolioId"):
                update_request = UpdateUserSettingsRequest(defaultPortfolioId="invalid-pf-id")
                UserService.update_user_settings(SAMPLE_UID, update_request)
