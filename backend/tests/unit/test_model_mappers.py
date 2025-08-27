import pytest
from uuid import uuid4, UUID
from datetime import datetime, timezone
from src.core.model_mappers import (
    userdb_to_user,
    update_user_settings_request_to_dict,
    portfolio_db_to_portfolio,
    portfolio_db_list_to_portfolio_list,
    cashreserve_db_to_cashreserve,
    portfolio_creation_request_to_dict,
    portfolio_update_request_to_dict,
    cashreserve_to_dict,
    portfolio_db_from_creation_request
)
from src.core.internal_models import UserDB, PortfolioDB, CashReserveDB, NotificationChannel
from src.api.models import (
    User, NotificationPreferences, Portfolio, CashReserve,
    UpdateUserSettingsRequest, PortfolioCreationRequest, PortfolioUpdateRequest, Currency
)

# --- Test Data ---
@pytest.fixture
def sample_user_db():
    """Provides a sample UserDB instance."""
    return UserDB(
        uid="test-user-123",
        username="testuser",
        email="test@example.com",
        defaultPortfolioId=uuid4(),
        subscriptionStatus="FREE",
        notificationPreferences=[NotificationChannel.EMAIL],
        createdAt=datetime.now(timezone.utc),
        modifiedAt=datetime.now(timezone.utc)
    )

@pytest.fixture
def sample_portfolio_db():
    """Provides a sample PortfolioDB instance."""
    return PortfolioDB(
        portfolioId=uuid4(),
        userId="test-user-123",
        name="Test Portfolio",
        description="Test Description",
        defaultCurrency="EUR",
        cashReserve=CashReserveDB(totalAmount=1000.0, warChestAmount=500.0),
        ruleSetId=None,
        createdAt=datetime.now(timezone.utc),
        modifiedAt=datetime.now(timezone.utc)
    )

@pytest.fixture
def sample_cashreserve_db():
    """Provides a sample CashReserveDB instance."""
    return CashReserveDB(totalAmount=1000.0, warChestAmount=500.0)

@pytest.fixture
def sample_update_user_settings_request():
    """Provides a sample UpdateUserSettingsRequest instance."""
    return UpdateUserSettingsRequest(
        defaultPortfolioId=uuid4(),
        notificationPreferences=NotificationPreferences(root=[NotificationChannel.PUSH, NotificationChannel.EMAIL])
    )

@pytest.fixture
def sample_portfolio_creation_request():
    """Provides a sample PortfolioCreationRequest instance."""
    return PortfolioCreationRequest(
        name="New Portfolio",
        description="New Description",
        defaultCurrency=Currency.EUR,
        cashReserve=CashReserve(totalAmount=2000.0, warChestAmount=1000.0)
    )

@pytest.fixture
def sample_portfolio_update_request():
    """Provides a sample PortfolioUpdateRequest instance."""
    return PortfolioUpdateRequest(
        name="Updated Portfolio",
        description="Updated Description",
        defaultCurrency=Currency.USD,
        cashReserve=CashReserve(totalAmount=3000.0, warChestAmount=1500.0)
    )

# --- Tests for userdb_to_user ---
def test_userdb_to_user(sample_user_db):
    """Test converting UserDB to User."""
    # ARRANGE
    user_db = sample_user_db

    # ACT
    user = userdb_to_user(user_db)

    # ASSERT
    assert isinstance(user, User)
    assert user.uid == user_db.uid
    assert user.username == user_db.username
    assert user.email == user_db.email
    assert user.defaultPortfolioId == user_db.defaultPortfolioId
    assert user.subscriptionStatus == user_db.subscriptionStatus
    assert user.notificationPreferences.root == [pref.value for pref in user_db.notificationPreferences]
    assert user.createdAt == user_db.createdAt
    assert user.modifiedAt == user_db.modifiedAt

# --- Tests for update_user_settings_request_to_dict ---
def test_update_user_settings_request_to_dict_full(sample_update_user_settings_request):
    """Test converting UpdateUserSettingsRequest with all fields."""
    # ARRANGE
    request = sample_update_user_settings_request

    # ACT
    result = update_user_settings_request_to_dict(request)

    # ASSERT
    assert isinstance(result, dict)
    assert result["defaultPortfolioId"] == request.defaultPortfolioId
    assert result["notificationPreferences"] == [NotificationChannel.PUSH.value, NotificationChannel.EMAIL.value]

def test_update_user_settings_request_to_dict_partial():
    """Test converting UpdateUserSettingsRequest with only defaultPortfolioId."""
    # ARRANGE
    request = UpdateUserSettingsRequest(defaultPortfolioId=uuid4())

    # ACT
    result = update_user_settings_request_to_dict(request)

    # ASSERT
    assert isinstance(result, dict)
    assert "defaultPortfolioId" in result
    assert "notificationPreferences" not in result

# --- Tests for portfolio_db_to_portfolio ---
def test_portfolio_db_to_portfolio(sample_portfolio_db):
    """Test converting PortfolioDB to Portfolio."""
    # ARRANGE
    portfolio_db = sample_portfolio_db

    # ACT
    portfolio = portfolio_db_to_portfolio(portfolio_db)

    # ASSERT
    assert isinstance(portfolio, Portfolio)
    assert portfolio.portfolioId == portfolio_db.portfolioId
    assert portfolio.userId == portfolio_db.userId
    assert portfolio.name == portfolio_db.name
    assert portfolio.description == portfolio_db.description
    assert portfolio.defaultCurrency == portfolio_db.defaultCurrency
    assert portfolio.cashReserve.totalAmount == portfolio_db.cashReserve.totalAmount
    assert portfolio.cashReserve.warChestAmount == portfolio_db.cashReserve.warChestAmount
    assert portfolio.ruleSetId == portfolio_db.ruleSetId
    assert portfolio.createdAt == portfolio_db.createdAt
    assert portfolio.modifiedAt == portfolio_db.modifiedAt

# --- Tests for portfolio_db_list_to_portfolio_list ---
def test_portfolio_db_list_to_portfolio_list(sample_portfolio_db):
    """Test converting List[PortfolioDB] to List[Portfolio]."""
    # ARRANGE
    portfolio_db_list = [sample_portfolio_db, sample_portfolio_db]

    # ACT
    portfolio_list = portfolio_db_list_to_portfolio_list(portfolio_db_list)

    # ASSERT
    assert isinstance(portfolio_list, list)
    assert len(portfolio_list) == 2
    assert all(isinstance(p, Portfolio) for p in portfolio_list)
    assert portfolio_list[0].portfolioId == portfolio_db_list[0].portfolioId
    assert portfolio_list[1].portfolioId == portfolio_db_list[1].portfolioId

# --- Tests for cashreserve_db_to_cashreserve ---
def test_cashreserve_db_to_cashreserve(sample_cashreserve_db):
    """Test converting CashReserveDB to CashReserve."""
    # ARRANGE
    cashreserve_db = sample_cashreserve_db

    # ACT
    cashreserve = cashreserve_db_to_cashreserve(cashreserve_db)

    # ASSERT
    assert isinstance(cashreserve, CashReserve)
    assert cashreserve.totalAmount == cashreserve_db.totalAmount
    assert cashreserve.warChestAmount == cashreserve_db.warChestAmount

# --- Tests for portfolio_creation_request_to_dict ---
def test_portfolio_creation_request_to_dict(sample_portfolio_creation_request):
    """Test converting PortfolioCreationRequest to dictionary."""
    # ARRANGE
    request = sample_portfolio_creation_request

    # ACT
    result = portfolio_creation_request_to_dict(request)

    # ASSERT
    assert isinstance(result, dict)
    assert result["name"] == request.name
    assert result["description"] == request.description
    assert result["defaultCurrency"] == request.defaultCurrency.value
    assert result["cashReserve"] == {"totalAmount": 2000.0, "warChestAmount": 1000.0}

# --- Tests for portfolio_update_request_to_dict ---
def test_portfolio_update_request_to_dict_full(sample_portfolio_update_request):
    """Test converting PortfolioUpdateRequest with all fields."""
    # ARRANGE
    request = sample_portfolio_update_request

    # ACT
    result = portfolio_update_request_to_dict(request)

    # ASSERT
    assert isinstance(result, dict)
    assert result["name"] == request.name
    assert result["description"] == request.description
    assert result["defaultCurrency"] == request.defaultCurrency.value
    assert result["cashReserve"] == {"totalAmount": 3000.0, "warChestAmount": 1500.0}

def test_portfolio_update_request_to_dict_partial():
    """Test converting PortfolioUpdateRequest with required fields only."""
    # ARRANGE
    request = PortfolioUpdateRequest(
        name="Partial Update",
        defaultCurrency=Currency.EUR,
        cashReserve=CashReserve(totalAmount=4000.0, warChestAmount=2000.0)
    )

    # ACT
    result = portfolio_update_request_to_dict(request)

    # ASSERT
    assert isinstance(result, dict)
    assert result["name"] == "Partial Update"
    assert result["defaultCurrency"] == Currency.EUR.value
    assert result["cashReserve"] == {"totalAmount": 4000.0, "warChestAmount": 2000.0}
    assert "description" not in result

# --- Tests for cashreserve_to_dict ---
def test_cashreserve_to_dict():
    """Test converting CashReserve to dictionary."""
    # ARRANGE
    cashreserve = CashReserve(totalAmount=4000.0, warChestAmount=2000.0)

    # ACT
    result = cashreserve_to_dict(cashreserve)

    # ASSERT
    assert isinstance(result, dict)
    assert result["totalAmount"] == 4000.0
    assert result["warChestAmount"] == 2000.0

# --- Tests for portfolio_db_from_creation_request ---
def test_portfolio_db_from_creation_request(sample_portfolio_creation_request):
    """Test converting PortfolioCreationRequest to PortfolioDB."""
    # ARRANGE
    request = sample_portfolio_creation_request
    user_id = "test-user-456"
    portfolio_id = uuid4()

    # ACT
    portfolio_db = portfolio_db_from_creation_request(request, user_id, portfolio_id)

    # ASSERT
    assert isinstance(portfolio_db, PortfolioDB)
    assert portfolio_db.portfolioId == portfolio_id
    assert portfolio_db.userId == user_id
    assert portfolio_db.name == request.name
    assert portfolio_db.description == request.description
    assert portfolio_db.defaultCurrency == request.defaultCurrency.value
    assert portfolio_db.cashReserve.totalAmount == request.cashReserve.totalAmount
    assert portfolio_db.cashReserve.warChestAmount == request.cashReserve.warChestAmount
    assert portfolio_db.ruleSetId is None
    assert isinstance(portfolio_db.createdAt, datetime)
    assert isinstance(portfolio_db.modifiedAt, datetime)
    
    