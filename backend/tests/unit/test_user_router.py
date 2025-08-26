import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from uuid import uuid4

client = TestClient(app)

def test_logout_user_success():
    """
    Test successful logout of a user.
    """
    # Use multiple patchers to mock 'auth' in every file that imports it
    with patch('src.middleware.auth') as mock_middleware_auth, \
         patch('src.dependencies.auth') as mock_dependencies_auth, \
         patch('src.routers.user_router.auth') as mock_router_auth:

        # 1. Configure the mock for the authentication checks
        decoded_token = {
            "uid": "test_uid",
            "email": "test@example.com",
            "name": "testuser"
        }
        # This covers the middleware AND the get_current_user dependency
        mock_middleware_auth.verify_id_token.return_value = decoded_token
        mock_dependencies_auth.verify_id_token.return_value = decoded_token

        # 2. Make the request
        headers = {
            "Authorization": "Bearer some_token",
            "Idempotency-Key": str(uuid4())
        }
        response = client.post("/api/v1/auth/logout", headers=headers)

        # 3. Assert the results
        assert response.status_code == 200
        assert response.json() == {"message": "U_I_4001: User logged out successfully."}
        
        # Assert that the router's 'auth' object was used to revoke tokens
        mock_router_auth.revoke_refresh_tokens.assert_called_once_with("test_uid")
        
        