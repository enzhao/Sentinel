from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from datetime import datetime, timezone
from typing import List

# Import the dependency functions we'll need
from ..dependencies import get_current_user, require_idempotency_key, get_user_service, get_portfolio_service
from ..api.models import User, UpdateUserSettingsRequest, Portfolio, PortfolioCreationRequest
from ..core.internal_models import CurrentUser
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

# Import the service classes for type hinting
from ..services.portfolio_service import PortfolioService
from ..services.user_service import UserService

# Import mappers
from ..core.model_mappers import userdb_to_user, update_user_settings_request_to_dict, portfolio_db_to_portfolio, portfolio_db_list_to_portfolio_list, portfolio_creation_request_to_dict

# Create the router directly instead of using a factory function
router = APIRouter()

@router.get("/users/me", response_model=User, summary="Retrieve current user's profile and settings")
async def get_current_user_profile(
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service) # Inject dependency here
):
    """
    Retrieves the full profile and settings for the currently authenticated user.
    Reference: product_spec.md#833-u_3000-api-request-authorization
    Reference: product_spec.md#932-us_2000-user-settings-retrieval
    """
    user_db = user_service.get_user_by_uid(current_user.uid)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )
    
    return userdb_to_user(user_db)

@router.get("/users/me/settings", response_model=User, summary="Retrieve current user's settings")
async def get_user_settings(
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service) # Inject dependency here
):
    """
    Retrieves the settings for the currently authenticated user.
    Reference: product_spec.md#932-us_2000-user-settings-retrieval
    """
    user_db = user_service.get_user_by_uid(current_user.uid)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found."
        )
    
    return userdb_to_user(user_db)

@router.put("/users/me/settings", response_model=User, summary="Update current user's settings")
async def update_user_settings(
    request: UpdateUserSettingsRequest,
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service), # Inject dependency here
    idempotency_key: UUID4 = Depends(require_idempotency_key)
):
    """
    Updates the settings for the currently authenticated user.
    Reference: product_spec.md#933-us_3000-user-settings-update
    """
    try:
        update_data = update_user_settings_request_to_dict(request)
        updated_user_db = user_service.update_user_settings(
            uid=current_user.uid,
            update_data=update_data
        )
        return userdb_to_user(updated_user_db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.post("/auth/logout", status_code=status.HTTP_200_OK, summary="Logout the current user and revoke refresh tokens")
async def logout_user(current_user: CurrentUser = Depends(get_current_user)):
    """
    Logs out the current user by revoking their Firebase refresh tokens.
    This invalidates all sessions for the user across all devices.
    Reference: product_spec.md#834-u_4000-user-logout
    """
    try:
        auth.revoke_refresh_tokens(current_user.uid)
        return {"message": "U_I_4001: User logged out successfully."}
    except FirebaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"U_E_4101: Failed to revoke refresh tokens: {e}"
        )

@router.post("/users/me/portfolios", response_model=Portfolio, status_code=status.HTTP_201_CREATED, summary="Create a new portfolio for the current user")
async def create_portfolio_for_user(
    request: PortfolioCreationRequest,
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service), # Inject dependency here
    idempotency_key: UUID4 = Depends(require_idempotency_key)
):
    """
    Creates a new portfolio for the authenticated user.
    Reference: product_spec.md#331-p_1000-portfolio-creation
    """
    # Check for existing portfolio with the same name for the user
    # This logic should ideally be inside the portfolio_service to keep the router clean
    # For now, we'll leave it as is to match your original file.
    # existing_portfolio = portfolio_service.get_portfolio_by_name_for_user(current_user.uid, request.name)
    # if existing_portfolio:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"P_E_1103: A portfolio with the name '{request.name}' already exists."
    #     )

    portfolio_data = portfolio_creation_request_to_dict(request)
    new_portfolio_db = portfolio_service.create_portfolio(user_id=current_user.uid, portfolio_data=portfolio_data)
    return portfolio_db_to_portfolio(new_portfolio_db)

@router.get("/users/me/portfolios", response_model=List[Portfolio], summary="Retrieve a list of all portfolios for the current user")
async def get_user_portfolios(
    current_user: CurrentUser = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service) # Inject dependency here
):
    """
    Retrieves a summary list of all portfolios owned by the authenticated user.
    Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval
    """
    portfolio_db_list = portfolio_service.get_portfolios_by_user(user_id=current_user.uid)
    return portfolio_db_list_to_portfolio_list(portfolio_db_list)

