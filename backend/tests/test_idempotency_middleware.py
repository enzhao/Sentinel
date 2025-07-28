import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid

# User 1
SAMPLE_USER_1 = {"uid": "test-user-idem-1", "email": "test1@example.com"}
# User 2
SAMPLE_USER_2 = {"uid": "test-user-idem-2", "email": "test2@example.com"}

def test_idempotency_replay(test_client: TestClient):
    """
    Happy Path: Confirms that replaying a request with the same key and user returns the stored response.
    """
    key = str(uuid.uuid4())
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_1):
        # First request
        response1 = test_client.post(
            "/api/portfolios",
            json={"name": "Idempotency Replay Test"},
            headers={"Authorization": "Bearer test-token-1", "Idempotency-Key": key}
        )
        assert response1.status_code == 201
        portfolio_id_1 = response1.json()["portfolioId"]

        # Second request with the same key
        response2 = test_client.post(
            "/api/portfolios",
            json={"name": "Idempotency Replay Test"},
            headers={"Authorization": "Bearer test-token-1", "Idempotency-Key": key}
        )
        assert response2.status_code == 201
        portfolio_id_2 = response2.json()["portfolioId"]
        
        # The portfolio ID should be identical, proving no new object was created
        assert portfolio_id_1 == portfolio_id_2

def test_idempotency_key_is_scoped_to_user(test_client: TestClient):
    """
    Error Path (Security): Confirms that the same key used by a different user is treated as a new request.
    """
    key = str(uuid.uuid4())
    # First request by User 1
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_1):
        response1 = test_client.post(
            "/api/portfolios",
            json={"name": "User Scope Test"},
            headers={"Authorization": "Bearer test-token-1", "Idempotency-Key": key}
        )
        assert response1.status_code == 201
        portfolio_id_1 = response1.json()["portfolioId"]

    # Second request by User 2 with the same key
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_2):
        response2 = test_client.post(
            "/api/portfolios",
            json={"name": "User Scope Test"},
            headers={"Authorization": "Bearer test-token-2", "Idempotency-Key": key}
        )
        assert response2.status_code == 201
        portfolio_id_2 = response2.json()["portfolioId"]

        # The portfolio IDs should be DIFFERENT, proving a new object was created
        assert portfolio_id_1 != portfolio_id_2

def test_get_requests_are_ignored_by_middleware(test_client: TestClient):
    """
    Happy Path: Confirms that GET requests are not affected by the idempotency middleware.
    """
    with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_1):
        # This GET request does not require an Idempotency-Key
        response = test_client.get(
            "/api/portfolios",
            headers={"Authorization": "Bearer test-token-1"}
        )
        assert response.status_code == 200
