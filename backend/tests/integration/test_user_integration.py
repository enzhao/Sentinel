import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid
from src.firebase_setup import db

# Define a unique user for this integration test to avoid conflicts.
# Using a UUID ensures the user is unique for each test run.
TEST_USER_UID = f"integration-test-user-{uuid.uuid4()}"
TEST_USER_EMAIL = f"{TEST_USER_UID}@test.com"
TEST_USERNAME = "integration_user"
SAMPLE_USER_AUTH = {"uid": TEST_USER_UID, "email": TEST_USER_EMAIL}

@pytest.fixture
def cleanup_firestore():
    """
    A fixture to handle the cleanup of Firestore documents after the test runs.
    This will run regardless of test success or failure.
    """
    # This is a generator fixture. The code before the `yield` is the setup,
    # and the code after is the teardown (cleanup).
    
    # Setup: No setup needed before the test.
    yield
    
    # Teardown: Cleanup logic starts here.
    print(f"\n--- Starting Firestore cleanup for user: {TEST_USER_UID} ---")
    
    # 1. Find the user document to get the defaultPortfolioId
    user_doc_ref = db.collection('users').document(TEST_USER_UID)
    user_doc = user_doc_ref.get()
    portfolio_id_to_delete = None

    if user_doc.exists:
        print(f"Found user document for {TEST_USER_UID}. Preparing to delete.")
        user_data = user_doc.to_dict()
        portfolio_id_to_delete = user_data.get('defaultPortfolioId')
        user_doc_ref.delete()
        print(f"Deleted user document: {TEST_USER_UID}")
    else:
        print(f"User document for {TEST_USER_UID} not found. It might have failed before creation or was already cleaned up.")

    # 2. Delete the associated default portfolio if it exists
    if portfolio_id_to_delete:
        portfolio_doc_ref = db.collection('portfolios').document(portfolio_id_to_delete)
        if portfolio_doc_ref.get().exists:
            portfolio_doc_ref.delete()
            print(f"Deleted portfolio document: {portfolio_id_to_delete}")
        else:
            print(f"Portfolio document {portfolio_id_to_delete} not found.")
    
    print("--- Firestore cleanup complete ---")


# def test_user_creation_and_cleanup(test_client: TestClient, cleanup_firestore):
#     """
#     Tests the end-to-end user creation process against a real Firestore database.
    
#     Steps:
#     1.  Calls the POST /api/users endpoint to create a user and default portfolio.
#     2.  Directly queries the real Firestore DB to verify the data was created correctly.
#     3.  The `cleanup_firestore` fixture ensures all created documents are deleted after the test.
#     """
#     # We only mock the auth verification, as we can't generate a real token in a test environment.
#     # The rest of the test interacts with the actual database.
#     with patch('firebase_admin.auth.verify_id_token', return_value=SAMPLE_USER_AUTH):
        
#         # --- 1. Call the API to initialize the user ---
#         response = test_client.post(
#             "/api/users",
#             json={"username": TEST_USERNAME},
#             headers={"Authorization": "Bearer dummy-token", "Idempotency-Key": str(uuid.uuid4())}
#         )
        
#         # --- 2. Assert the API call was successful ---
#         assert response.status_code == 201
#         response_data = response.json()
#         assert response_data["uid"] == TEST_USER_UID
#         assert response_data["email"] == TEST_USER_EMAIL
#         assert response_data["username"] == TEST_USERNAME
#         assert response_data["defaultPortfolioId"] is not None
        
#         default_portfolio_id = response_data["defaultPortfolioId"]
        
#         # --- 3. Directly verify data in the real Firestore database ---
#         print(f"\nVerifying data in Firestore for user {TEST_USER_UID}...")

#         # Verify user document
#         user_doc = db.collection('users').document(TEST_USER_UID).get()
#         assert user_doc.exists, "User document was not created in Firestore."
#         user_data = user_doc.to_dict()
#         assert user_data["email"] == TEST_USER_EMAIL
#         assert user_data["username"] == TEST_USERNAME
#         assert user_data["defaultPortfolioId"] == default_portfolio_id
#         print("User document verified successfully.")

#         # Verify portfolio document
#         portfolio_doc = db.collection('portfolios').document(default_portfolio_id).get()
#         assert portfolio_doc.exists, "Default portfolio document was not created in Firestore."
#         portfolio_data = portfolio_doc.to_dict()
#         assert portfolio_data["userId"] == TEST_USER_UID
#         assert portfolio_data["name"] == "My First Portfolio"
#         print("Portfolio document verified successfully.")

