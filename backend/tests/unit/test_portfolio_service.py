import pytest
from uuid import uuid4, UUID
from datetime import datetime, timezone
from firebase_admin import firestore

# Import the services and models we are going to test
from src.services.user_service import UserService
from src.services.portfolio_service import PortfolioService
from src.core.internal_models import PortfolioDB, CashReserveDB

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
def test_user(db_client: firestore.Client) -> dict:
    """Creates a user document in Firestore for testing and yields the user data."""
    user_id = f"service-test-user-{uuid4()}"
    user_data = {
        "uid": user_id,
        "email": f"{user_id}@example.com",
        "username": "Service Test User",
        "defaultPortfolioId": None,
    }
    db_client.collection("users").document(user_id).set(user_data)
    yield user_data

@pytest.fixture(scope="function")
def created_portfolio(portfolio_service: PortfolioService, test_user: dict) -> PortfolioDB:
    """Creates a portfolio using the service and yields the resulting PortfolioDB object."""
    user_id = test_user["uid"]
    portfolio_data = {
        "name": "My Service Test Portfolio",
        "description": "A portfolio created via the service.",
        "defaultCurrency": "USD",
        "cashReserve": {"totalAmount": 1000.0, "warChestAmount": 200.0}
    }
    new_portfolio = portfolio_service.create_portfolio(user_id, portfolio_data)
    yield new_portfolio

# --- Unit Tests for PortfolioService ---

def test_create_portfolio_success(portfolio_service: PortfolioService, test_user: dict):
    """
    Tests that a portfolio can be successfully created.
    """
    # ARRANGE
    user_id = test_user["uid"]
    portfolio_data = {
        "name": "My New Portfolio",
        "description": "For testing creation",
        "defaultCurrency": "EUR",
        "cashReserve": {"totalAmount": 5000, "warChestAmount": 1000}
    }

    # ACT
    new_portfolio = portfolio_service.create_portfolio(user_id, portfolio_data)

    # ASSERT
    assert new_portfolio is not None
    assert isinstance(new_portfolio, PortfolioDB)
    assert new_portfolio.userId == user_id
    assert new_portfolio.name == "My New Portfolio"
    assert new_portfolio.cashReserve.totalAmount == 5000

def test_get_portfolio_by_id_success(portfolio_service: PortfolioService, created_portfolio: PortfolioDB):
    """
    Tests retrieving a portfolio by its ID.
    """
    # ARRANGE
    portfolio_id = created_portfolio.portfolioId

    # ACT
    retrieved_portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    # ASSERT
    assert retrieved_portfolio is not None
    assert retrieved_portfolio.portfolioId == portfolio_id
    assert retrieved_portfolio.name == created_portfolio.name

def test_get_portfolio_by_name_success(portfolio_service: PortfolioService, created_portfolio: PortfolioDB):
    """
    Tests retrieving a portfolio by its name for a specific user.
    """
    # ARRANGE
    user_id = created_portfolio.userId
    portfolio_name = created_portfolio.name

    # ACT
    retrieved_portfolio = portfolio_service.get_portfolio_by_name(user_id, portfolio_name)

    # ASSERT
    assert retrieved_portfolio is not None
    assert retrieved_portfolio.userId == user_id
    assert retrieved_portfolio.name == portfolio_name

def test_get_portfolios_by_user(portfolio_service: PortfolioService, test_user: dict):
    """
    Tests retrieving all portfolios for a user.
    """
    # ARRANGE
    user_id = test_user["uid"]
    portfolio_service.create_portfolio(user_id, {"name": "Portfolio 1", "defaultCurrency": "USD", "cashReserve": {"totalAmount": 100, "warChestAmount": 10}})
    portfolio_service.create_portfolio(user_id, {"name": "Portfolio 2", "defaultCurrency": "EUR", "cashReserve": {"totalAmount": 200, "warChestAmount": 20}})

    # ACT
    portfolios = portfolio_service.get_portfolios_by_user(user_id)

    # ASSERT
    assert len(portfolios) == 2
    assert all(isinstance(p, PortfolioDB) for p in portfolios)
    assert {p.name for p in portfolios} == {"Portfolio 1", "Portfolio 2"}

def test_update_portfolio_success(portfolio_service: PortfolioService, created_portfolio: PortfolioDB):
    """
    Tests updating a portfolio's details.
    """
    # ARRANGE
    portfolio_id = created_portfolio.portfolioId
    update_data = {
        "name": "Updated Name",
        "description": "Updated Description"
    }

    # ACT
    updated_portfolio = portfolio_service.update_portfolio(portfolio_id, update_data)

    # ASSERT
    assert updated_portfolio is not None
    assert updated_portfolio.portfolioId == portfolio_id
    assert updated_portfolio.name == "Updated Name"
    assert updated_portfolio.description == "Updated Description"
    assert updated_portfolio.modifiedAt > created_portfolio.modifiedAt

def test_delete_portfolio_success(portfolio_service: PortfolioService, user_service: UserService, created_portfolio: PortfolioDB):
    """
    Tests that a portfolio is successfully deleted.
    """
    # ARRANGE
    user_id = created_portfolio.userId
    portfolio_id = created_portfolio.portfolioId

    # ACT
    portfolio_service.delete_portfolio(user_id, portfolio_id, user_service)

    # ASSERT
    deleted_portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    assert deleted_portfolio is None

def test_delete_portfolio_reassigns_default(portfolio_service: PortfolioService, user_service: UserService, db_client: firestore.Client, test_user: dict):
    """
    Tests that deleting a default portfolio reassigns the default to another one.
    """
    # ARRANGE
    user_id = test_user["uid"]
    
    # 1. Create two portfolios
    p1_data = {"name": "Portfolio One", "defaultCurrency": "USD", "cashReserve": {"totalAmount": 100, "warChestAmount": 10}}
    p2_data = {"name": "Portfolio Two", "defaultCurrency": "EUR", "cashReserve": {"totalAmount": 200, "warChestAmount": 20}}
    portfolio1 = portfolio_service.create_portfolio(user_id, p1_data)
    portfolio2 = portfolio_service.create_portfolio(user_id, p2_data)

    # 2. Set portfolio1 as the default
    user_service.update_user_settings(user_id, {"defaultPortfolioId": portfolio1.portfolioId})
    user_before = user_service.get_user_by_uid(user_id)
    assert user_before.defaultPortfolioId == portfolio1.portfolioId

    # ACT: Delete the default portfolio
    portfolio_service.delete_portfolio(user_id, portfolio1.portfolioId, user_service)

    # ASSERT
    # 1. Check that portfolio1 is gone
    assert portfolio_service.get_portfolio_by_id(portfolio1.portfolioId) is None
    # 2. Check that the user's default has been updated to portfolio2
    user_after = user_service.get_user_by_uid(user_id)
    assert user_after.defaultPortfolioId == portfolio2.portfolioId

def test_delete_portfolio_sets_default_to_none(portfolio_service: PortfolioService, user_service: UserService, created_portfolio: PortfolioDB):
    """
    Tests that deleting the only portfolio (which is the default) sets the user's default to None.
    """
    # ARRANGE
    user_id = created_portfolio.userId
    portfolio_id = created_portfolio.portfolioId

    # 1. Set the created portfolio as the default
    user_service.update_user_settings(user_id, {"defaultPortfolioId": portfolio_id})
    user_before = user_service.get_user_by_uid(user_id)
    assert user_before.defaultPortfolioId == portfolio_id

    # ACT: Delete the only portfolio
    portfolio_service.delete_portfolio(user_id, portfolio_id, user_service)

    # ASSERT
    user_after = user_service.get_user_by_uid(user_id)
    assert user_after.defaultPortfolioId is None