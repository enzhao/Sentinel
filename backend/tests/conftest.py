# conftest.py
import pytest
import os
from fastapi.testclient import TestClient
import requests

# Set environment variables for the emulator BEFORE any firebase imports
# We explicitly use a 'test' environment for running tests to distinguish
# it from the 'dev' environment used for the local development server.
os.environ["ENV"] = "test"
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"
os.environ["GCLOUD_PROJECT"] = "sentinel-invest"

# Now we can safely import from our application
from src.firebase_setup import initialize_firebase_app, get_db_client
from src.dependencies import get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Initializes the Firebase app for the entire test session.
    """
    initialize_firebase_app()
    yield

@pytest.fixture(scope="module")
def db_client():
    """
    Provides a Firestore client for the test module.
    """
    return get_db_client()

@pytest.fixture(scope="module")
def test_client(db_client) -> TestClient:
    """
    Provides a TestClient for making API requests, with the database
    dependency overridden to point to the emulator.
    """
    # Import the app here to prevent premature configuration.
    from src.main import app

    app.dependency_overrides[get_db] = lambda: db_client

    with TestClient(app) as client:
        yield client

    # Clear the override after the tests in this module are done.
    app.dependency_overrides = {}

@pytest.fixture(scope="function", autouse=True)
def clear_firestore_emulator(db_client):
    """
    Clears all data in the Firestore emulator before each test function.
    This ensures test isolation.
    """
    try:
        # This is a robust way to clear the emulator
        requests.delete(f"http://{os.environ['FIRESTORE_EMULATOR_HOST']}/emulator/v1/projects/{os.environ['GCLOUD_PROJECT']}/databases/(default)/documents")
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Could not connect to Firestore emulator. Is it running? Details: {e}")
    yield
