from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.auth import get_current_user
from src.services.portfolio_service import portfolio_service
from src.services.user_service import user_service
from src.models import (
    CreatePortfolioRequest,
    Portfolio,
    User,
    UpdateUserSettingsRequest,
    UpdatePortfolioRequest,
    AddHoldingRequest,
    InitializeUserRequest
)
from src.dependencies import require_idempotency_key
from src.services.enrichment_service import enrichment_service

router = APIRouter(
    tags=["Users & Portfolios"],
    dependencies=[Depends(get_current_user)]
)

# ======================================================================================
# User Management Endpoints
# ======================================================================================

# @router.post("/users", status_code=status.HTTP_201_CREATED, response_model=User, summary="Create User and Default Portfolio")
# def create_user_and_portfolio(
#     request: InitializeUserRequest,
#     current_user: dict = Depends(get_current_user),
#     _idempotency_key: str = Depends(require_idempotency_key)
# ):
#     """
#     Handles the one-time initialization of a new user after they have signed up
#     via Firebase Authentication.

#     This endpoint:
#     1.  Verifies the user's ID token.
#     2.  Checks if a user document already exists in Firestore. If so, it returns
#         the existing user, enforcing idempotency.
#     3.  If the user is new, it creates a `User` document in Firestore with their
#         UID, email, and chosen username.
#     4.  Creates a default portfolio for the new user (e.g., "My First Portfolio").
#     5.  Links the default portfolio to the user by setting `defaultPortfolioId`.
#     6.  Returns the newly created and fully initialized `User` object.
#     """
#     uid = current_user["uid"]
#     email = current_user.get("email")

#     # Idempotency check: If user already exists, return them.
#     existing_user = user_service.get_user(uid)
#     if existing_user:
#         return existing_user

#     # Create the user document in Firestore
#     new_user = user_service.create_user(uid=uid, email=email, username=request.username)
#     if not new_user:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user.")

#     # Create the default portfolio
#     default_portfolio_data = CreatePortfolioRequest(name="My First Portfolio")
#     new_portfolio = portfolio_service.create_portfolio(
#         user_id=uid,
#         portfolio_data=default_portfolio_data
#     )
#     if not new_portfolio:
#         # This case should ideally not be reached if user creation was successful
#         # and portfolio name is not a duplicate for a new user.
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create default portfolio.")

#     # Link the portfolio and update the user
#     update_settings = UpdateUserSettingsRequest(defaultPortfolioId=new_portfolio.portfolioId)
#     updated_user = user_service.update_user_settings(uid, update_settings)
#     if not updated_user:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to link default portfolio to user.")

#     return updated_user

@router.get("/users/me", response_model=User)
def get_user_me(current_user: dict = Depends(get_current_user)):
    """
    Get the current authenticated user's details.
    """
    user = user_service.get_user(current_user["uid"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/me/settings", response_model=User)
def update_user_settings(
    settings: UpdateUserSettingsRequest,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Update the current user's settings, including their default portfolio.
    """
    uid = current_user["uid"]
    try:
        updated_user = user_service.update_user_settings(uid, settings)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ======================================================================================
# Portfolio Management Endpoints (Nested under the user)
# ======================================================================================

@router.post("/users/me/portfolios", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_data: CreatePortfolioRequest,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Create a new portfolio for the authenticated user.
    """
    new_portfolio_db = portfolio_service.create_portfolio(current_user["uid"], portfolio_data)
    if not new_portfolio_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A portfolio with the name '{portfolio_data.name}' already exists."
        )
    return Portfolio(**new_portfolio_db.model_dump())

@router.get("/users/me/portfolios", response_model=List[Portfolio])
def get_all_portfolios(
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a summary list of all of the user's portfolios.
    """
    portfolios_db = portfolio_service.get_portfolios_by_user(current_user["uid"])
    enriched_portfolios = [enrichment_service.enrich_portfolio(p) for p in portfolios_db]
    return enriched_portfolios

@router.get("/users/me/portfolios/{portfolio_id}", response_model=Portfolio)
def get_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve the full, enriched details of a single portfolio.
    """
    portfolio_db = portfolio_service.get_portfolio_by_id(portfolio_id, current_user["uid"])
    if not portfolio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    
    enriched_portfolio = enrichment_service.enrich_portfolio(portfolio_db)
    return enriched_portfolio

@router.put("/users/me/portfolios/{portfolio_id}", response_model=Portfolio)
def update_portfolio(
    portfolio_id: str,
    update_data: UpdatePortfolioRequest,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Update a portfolio's name, cash reserves, or tax settings.
    """
    updated_portfolio_db = portfolio_service.update_portfolio(portfolio_id, current_user["uid"], update_data)
    if not updated_portfolio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    
    enriched_portfolio = enrichment_service.enrich_portfolio(updated_portfolio_db)
    return enriched_portfolio

@router.delete("/users/me/portfolios/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Delete an entire portfolio.
    """
    success = portfolio_service.delete_portfolio(portfolio_id, current_user["uid"])
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return

# ======================================================================================
# Holdings and Lots Management Endpoints (Nested under portfolio)
# ======================================================================================

@router.post("/users/me/portfolios/{portfolio_id}/holdings", response_model=Portfolio)
def add_holding_to_portfolio(
    portfolio_id: str,
    holding_data: AddHoldingRequest,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Add a new holding with lots to a portfolio.
    """
    try:
        updated_portfolio_db = portfolio_service.add_holding(portfolio_id, current_user["uid"], holding_data)
        if not updated_portfolio_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
        
        enriched_portfolio = enrichment_service.enrich_portfolio(updated_portfolio_db)
        return enriched_portfolio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/users/me/portfolios/{portfolio_id}/holdings/{holding_id}", response_model=Portfolio)
def delete_holding_from_portfolio(
    portfolio_id: str,
    holding_id: str,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Delete a holding from a portfolio.
    """
    updated_portfolio_db = portfolio_service.delete_holding(portfolio_id, current_user["uid"], holding_id)
    if not updated_portfolio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found in the specified portfolio.")
    
    enriched_portfolio = enrichment_service.enrich_portfolio(updated_portfolio_db)
    return enriched_portfolio

@router.delete("/users/me/portfolios/{portfolio_id}/holdings/{holding_id}/lots/{lot_id}", response_model=Portfolio)
def delete_lot_from_holding(
    portfolio_id: str,
    holding_id: str,
    lot_id: str,
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Delete a lot from a holding within a portfolio.
    """
    updated_portfolio_db = portfolio_service.delete_lot(portfolio_id, current_user["uid"], holding_id, lot_id)
    if not updated_portfolio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found in the specified holding.")
        
    enriched_portfolio = enrichment_service.enrich_portfolio(updated_portfolio_db)
    return enriched_portfolio
