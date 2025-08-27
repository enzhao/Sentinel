from src.api.models import (
    User, NotificationPreferences, Portfolio, CashReserve,
    UpdateUserSettingsRequest, PortfolioCreationRequest,
    PortfolioUpdateRequest
)
from src.core.internal_models import UserDB, PortfolioDB, CashReserveDB
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timezone

def userdb_to_user(user_db: UserDB) -> User:
    """Convert a UserDB (internal) to a User (API) model."""
    return User.model_validate({
        "uid": user_db.uid,
        "username": user_db.username,
        "email": user_db.email,
        "defaultPortfolioId": user_db.defaultPortfolioId,
        "subscriptionStatus": user_db.subscriptionStatus,
        "notificationPreferences": NotificationPreferences(root=user_db.notificationPreferences),
        "createdAt": user_db.createdAt,
        "modifiedAt": user_db.modifiedAt
    })

def update_user_settings_request_to_dict(request: UpdateUserSettingsRequest) -> Dict[str, Any]:
    """Convert an UpdateUserSettingsRequest (API) to a dictionary for UserService."""
    data = request.model_dump(exclude_unset=True)
    return data

def portfolio_db_to_portfolio(portfolio_db: PortfolioDB) -> Portfolio:
    """Convert a PortfolioDB (internal) to a Portfolio (API) model."""
    return Portfolio.model_validate({
        "portfolioId": portfolio_db.portfolioId,
        "userId": portfolio_db.userId,
        "name": portfolio_db.name,
        "description": portfolio_db.description,
        "defaultCurrency": portfolio_db.defaultCurrency,
        "cashReserve": cashreserve_db_to_cashreserve(portfolio_db.cashReserve),
        "ruleSetId": portfolio_db.ruleSetId,
        "createdAt": portfolio_db.createdAt,
        "modifiedAt": portfolio_db.modifiedAt
    })

def portfolio_db_list_to_portfolio_list(portfolio_db_list: List[PortfolioDB]) -> List[Portfolio]:
    """Convert a list of PortfolioDB (internal) to a list of Portfolio (API) models."""
    return [portfolio_db_to_portfolio(portfolio_db) for portfolio_db in portfolio_db_list]

def cashreserve_db_to_cashreserve(cashreserve_db: CashReserveDB) -> CashReserve:
    """Convert a CashReserveDB (internal) to a CashReserve (API) model."""
    return CashReserve.model_validate({
        "totalAmount": cashreserve_db.totalAmount,
        "warChestAmount": cashreserve_db.warChestAmount
    })

def portfolio_creation_request_to_dict(request: PortfolioCreationRequest) -> Dict[str, Any]:
    """Convert a PortfolioCreationRequest (API) to a dictionary for PortfolioService."""
    data = request.model_dump(exclude_unset=True)
    # cashReserve is already a dict from model_dump, no need to convert again
    return data

def portfolio_update_request_to_dict(request: PortfolioUpdateRequest) -> Dict[str, Any]:
    """Convert a PortfolioUpdateRequest (API) to a dictionary for PortfolioService."""
    data = request.model_dump(exclude_unset=True)
    # cashReserve is already a dict from model_dump, no need to convert again
    return data

def cashreserve_to_dict(cashreserve: CashReserve) -> Dict[str, Any]:
    """Convert a CashReserve (API) to a dictionary for Firestore."""
    return {
        "totalAmount": cashreserve.totalAmount,
        "warChestAmount": cashreserve.warChestAmount
    }

def portfolio_db_from_creation_request(request: PortfolioCreationRequest, user_id: str, portfolio_id: UUID) -> PortfolioDB:
    """Convert a PortfolioCreationRequest to a PortfolioDB for Firestore."""
    now = datetime.now(timezone.utc)
    return PortfolioDB(
        portfolioId=portfolio_id,
        userId=user_id,
        name=request.name,
        description=request.description,
        defaultCurrency=request.defaultCurrency,
        cashReserve=CashReserveDB(
            totalAmount=request.cashReserve.totalAmount,
            warChestAmount=request.cashReserve.warChestAmount
        ),
        ruleSetId=None,
        createdAt=now,
        modifiedAt=now
    )
    
    