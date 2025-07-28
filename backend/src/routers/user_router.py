from fastapi import APIRouter, Depends, status
from src.auth import get_current_user
from src.services.portfolio_service import portfolio_service
from src.models import CreatePortfolioRequest, Portfolio
from src.dependencies import require_idempotency_key

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/initialize", status_code=status.HTTP_200_OK, response_model=Portfolio)
def initialize_user_portfolio(
    current_user: dict = Depends(get_current_user),
    _idempotency_key: str = Depends(require_idempotency_key)
):
    """
    Initializes the user's account by creating a default portfolio if one doesn't exist.
    This endpoint is idempotent.
    """
    # Check if the user already has any portfolios
    existing_portfolios = portfolio_service.get_portfolios_by_user(current_user["uid"])
    if existing_portfolios:
        # If they do, return the first one.
        return existing_portfolios[0]

    # If no portfolios exist, create the default one.
    default_portfolio_data = CreatePortfolioRequest(name="My First Portfolio")
    new_portfolio = portfolio_service.create_portfolio(
        user_id=current_user["uid"],
        portfolio_data=default_portfolio_data
    )
    return new_portfolio
