from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import UUID4
from typing import List

from src.api.models import (
    Portfolio,
    PortfolioCreationRequest,
    PortfolioSummary,
    PortfolioUpdateRequest,
    DailyPortfolioSnapshot
)
from src.core.internal_models import CurrentUser
from src.dependencies import get_current_user, get_portfolio_service, get_user_service, require_idempotency_key
from src.services.portfolio_service import PortfolioService
import src.core.model_mappers as model_mappers
from src.messages import get_message

router = APIRouter(
    prefix="/users/me/portfolios",
    tags=["Portfolios"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "",
    response_model=Portfolio,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new portfolio",
    description="Reference: product_spec.md#3.3.1-P_1000-Portfolio-Creation",
    responses={
        409: {"description": "A portfolio with the same name already exists for the user."},
        401: {"description": "User is not authenticated."},
        400: {"description": "Invalid request data."},
    }
)
def create_portfolio(
    request: PortfolioCreationRequest,
    idempotency_key: UUID4 = Depends(require_idempotency_key),
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
) -> Portfolio:
    """
    Creates a new portfolio for the authenticated user.
    - **P_I_1001**: Creation succeeds.
    - **P_E_1103**: Name not unique.
    - **P_E_1104**: Invalid default currency (handled by Pydantic).
    - **P_E_1105**: Idempotency key missing/invalid (handled by dependency).
    """
    # P_E_1103: Check if a portfolio with the same name already exists for the user.
    if portfolio_service.get_portfolio_by_name(current_user.uid, request.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=get_message("P_E_1103", name=request.name),
        )

    portfolio_dict = model_mappers.portfolio_creation_request_to_dict(request)
    new_portfolio_db = portfolio_service.create_portfolio(current_user.uid, portfolio_dict)
    return model_mappers.portfolio_db_to_portfolio(new_portfolio_db)


@router.get(
    "",
    response_model=List[PortfolioSummary],
    summary="Retrieve a list of all portfolios for the authenticated user",
    description="Reference: product_spec.md#3.3.2.2-P_2200-Portfolio-List-Retrieval",
)
def list_portfolios(
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
) -> List[PortfolioSummary]:
    """
    Retrieves a summary list of all portfolios owned by the authenticated user.
    - **P_I_2201**: List retrieval succeeds.
    - **P_E_2301**: User unauthorized (handled by dependency).
    """
    portfolios_db = portfolio_service.get_portfolios_by_user(current_user.uid)
    return model_mappers.portfolio_db_list_to_portfolio_summary_list(portfolios_db)


@router.get(
    "/{portfolio_id}",
    response_model=Portfolio,
    summary="Retrieve a single portfolio by ID",
    description="Reference: product_spec.md#3.3.2.1-P_2000-Single-Portfolio-Retrieval",
)
def get_portfolio_by_id(
    portfolio_id: UUID4,
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
) -> Portfolio:
    """
    Retrieves the full, detailed content of a single portfolio for the authenticated user.
    - **P_I_2001**: Single retrieval succeeds.
    - **P_E_2101**: User unauthorized.
    - **P_E_2102**: Portfolio not found.
    """
    portfolio_db = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=get_message("P_E_2102", portfolioId=portfolio_id))
    if portfolio_db.userId != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=get_message("P_E_2101", portfolioId=portfolio_id))
    return model_mappers.portfolio_db_to_portfolio(portfolio_db)


@router.put(
    "/{portfolio_id}",
    response_model=Portfolio,
    summary="Update a specific portfolio's settings",
    description="Reference: product_spec.md#3.3.3.1-P_3000-Portfolio-Update-(Manual)",
)
def update_portfolio(
    portfolio_id: UUID4,
    request: PortfolioUpdateRequest,
    idempotency_key: UUID4 = Depends(require_idempotency_key),
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
) -> Portfolio:
    """
    Updates a specific portfolio's settings (like name, description, or cash reserves).
    - **P_I_3001**: Update succeeds.
    - **P_E_3101**: User unauthorized.
    - **P_E_3102**: Portfolio not found.
    - **P_E_3103**: Invalid cash amounts.
    - **P_E_3104**: Invalid portfolio settings (e.g., duplicate name).
    """
    # P_E_3102: Check if portfolio exists
    portfolio_to_update = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=get_message("P_E_2102", portfolioId=portfolio_id))

    # P_E_3101: Check ownership
    if portfolio_to_update.userId != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=get_message("P_E_2101", portfolioId=portfolio_id))

    # P_E_3104: Check for name conflict if the name is being changed
    if request.name and request.name != portfolio_to_update.name:
        existing_portfolio = portfolio_service.get_portfolio_by_name(current_user.uid, request.name)
        if existing_portfolio and existing_portfolio.portfolioId != portfolio_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=get_message("P_E_1103", name=request.name))

    # P_E_3103: Validate cash reserve amounts
    if request.cashReserve:
        if request.cashReserve.totalAmount < 0 or request.cashReserve.warChestAmount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=get_message("P_E_3103"))
        if request.cashReserve.warChestAmount > request.cashReserve.totalAmount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=get_message("P_E_3103"))

    update_dict = model_mappers.portfolio_update_request_to_dict(request)
    updated_portfolio_db = portfolio_service.update_portfolio(portfolio_id, update_dict)

    if not updated_portfolio_db:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=get_message("P_E_2102", portfolioId=portfolio_id))

    return model_mappers.portfolio_db_to_portfolio(updated_portfolio_db)


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an entire portfolio",
    description="Reference: product_spec.md#3.3.4.1-P_4000-Portfolio-Deletion-(Entire-Portfolio)",
)
def delete_portfolio(
    portfolio_id: UUID4,
    idempotency_key: UUID4 = Depends(require_idempotency_key),
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    user_service = Depends(get_user_service)
):
    """
    Deletes an entire portfolio and all of its associated holdings and data.
    - **P_I_4001**: Portfolio deletion succeeds.
    - **P_E_4101**: User unauthorized.
    - **P_E_4102**: Portfolio not found.
    """
    # P_E_4102: Check if portfolio exists
    portfolio_to_delete = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio_to_delete:
        # Return 204 even if not found to ensure idempotency.
        # The resource is gone, which is the desired state.
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # P_E_4101: Check ownership
    if portfolio_to_delete.userId != current_user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=get_message("P_E_4101", portfolioId=portfolio_id))

    portfolio_service.delete_portfolio(current_user.uid, portfolio_id, user_service)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{portfolio_id}/chart-data",
    response_model=List[DailyPortfolioSnapshot],
    summary="Retrieve time-series performance data for a portfolio",
    description="Reference: product_spec.md#3.3.2.3-P_2400-Portfolio-Chart-Data-Retrieval",
)
def get_portfolio_chart_data(
    portfolio_id: UUID4,
    range: str,
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
) -> List[DailyPortfolioSnapshot]:
    # As per spec, this will return empty data for now as snapshots are not generated.
    return []