import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

# In-memory "database" for testing
mock_db_data = {}

def mock_set(data):
    # document_id is the key
    document_id = mock_db_data['current_doc_id']
    mock_db_data[document_id] = data

def mock_get():
    document_id = mock_db_data['current_doc_id']
    doc_data = mock_db_data.get(document_id)
    
    mock_doc = MagicMock()
    mock_doc.exists = doc_data is not None
    mock_doc.to_dict.return_value = doc_data or {}
    return mock_doc

def mock_document(document_id):
    mock_db_data['current_doc_id'] = document_id
    mock_doc_ref = MagicMock()
    mock_doc_ref.set = mock_set
    mock_doc_ref.get = mock_get
    return mock_doc_ref

# Mock the firebase_admin library
mock_firebase_admin = MagicMock()
mock_firebase_admin.firestore.client.return_value.collection.return_value.document = mock_document

patcher = patch.dict('sys.modules', {
    'firebase_admin': mock_firebase_admin,
    'firebase_admin.credentials': mock_firebase_admin.credentials,
    'firebase_admin.firestore': mock_firebase_admin.firestore,
    'firebase_admin.auth': mock_firebase_admin.auth,
})
patcher.start()

# Now we can safely import our app
from src.main import app

@pytest.fixture(scope="function", autouse=True)
def clear_mock_db():
    """Clears the mock database before each test function."""
    global mock_db_data
    mock_db_data.clear()

@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    A fixture to provide a test client for the FastAPI app.
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
async def async_test_client() -> AsyncClient:
    """
    A fixture to provide an async test client for the FastAPI app.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Stop patching after all tests are done
@pytest.fixture(scope="session", autouse=True)
def stop_patcher(request):
    """Stop the patcher after all tests are done."""
    def finalizer():
        patcher.stop()
    request.addfinalizer(finalizer)