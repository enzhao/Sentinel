from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models import (
    CreatePortfolioRequest,
    Portfolio,
    UpdatePortfolioRequest,
    AddHoldingRequest
)
from src.portfolio_service import portfolio_service
from src.auth import get_current_user
from src.enrichment_service import enrichment_service
from src.dependencies import require_idempotency_key

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
    dependencies=[Depends(get_current_user)]
)

@router.post("", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
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

@router.get("", response_model=List[Portfolio])
def get_all_portfolios(
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a summary list of all of the user's portfolios.
    """
    portfolios_db = portfolio_service.get_portfolios_by_user(current_user["uid"])
    enriched_portfolios = [enrichment_service.enrich_portfolio(p) for p in portfolios_db]
    return enriched_portfolios

@router.get("/{portfolio_id}", response_model=Portfolio)
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

@router.put("/{portfolio_id}", response_model=Portfolio)
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

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.post("/{portfolio_id}/holdings", response_model=Portfolio)
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

@router.delete("/{portfolio_id}/holdings/{holding_id}", response_model=Portfolio)
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

@router.delete("/{portfolio_id}/holdings/{holding_id}/lots/{lot_id}", response_model=Portfolio)
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
