from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from datetime import datetime, timezone
from typing import List

from ..dependencies import get_current_user, require_idempotency_key
from ..firebase_setup import db
from ..api.models import User, UpdateUserSettingsRequest, Portfolio, Currency, CashReserve, SubscriptionStatus, NotificationPreferences, PortfolioCreationRequest, PortfolioSummary
from ..core.internal_models import CurrentUser
from ..core.utils import convert_uuids_to_str
from ..services.portfolio_service import portfolio_service # Import portfolio_service
from firebase_admin import auth

router = APIRouter()

@router.get("/users/me", response_model=User, summary="Retrieve current user's profile and settings")
async def get_current_user_profile(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves the full profile and settings for the currently authenticated user.
    Reference: product_spec.md#833-u_3000-api-request-authorization
    Reference: product_spec.md#932-us_2000-user-settings-retrieval
    """
    user_doc_ref = db.collection("users").document(current_user.uid)
    user_doc = user_doc_ref.get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )
    
    return User(**user_doc.to_dict())

@router.get("/users/me/settings", response_model=User, summary="Retrieve current user's settings")
async def get_user_settings(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves the settings for the currently authenticated user.
    Reference: product_spec.md#932-us_2000-user-settings-retrieval
    """
    user_doc_ref = db.collection("users").document(current_user.uid)
    user_doc = user_doc_ref.get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found."
        )
    
    return User(**user_doc.to_dict())

@router.put("/users/me/settings", response_model=User, summary="Update current user's settings")
async def update_user_settings(
    request: UpdateUserSettingsRequest,
    current_user: CurrentUser = Depends(get_current_user),
    idempotency_key: UUID4 = Depends(require_idempotency_key)
):
    """
    Updates the settings for the currently authenticated user.
    Reference: product_spec.md#933-us_3000-user-settings-update
    """
    user_doc_ref = db.collection("users").document(current_user.uid)

    # Check if the defaultPortfolioId exists and belongs to the user
    if request.defaultPortfolioId:
        portfolio_doc_ref = db.collection("portfolios").document(str(request.defaultPortfolioId))
        portfolio_doc = portfolio_doc_ref.get()
        if not portfolio_doc.exists or portfolio_doc.to_dict().get("userId") != current_user.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="US_E_3102: Invalid default portfolio specified."
            )

    update_data = request.model_dump(exclude_unset=True)
    update_data["modifiedAt"] = datetime.now(timezone.utc)

    user_doc_ref.update(convert_uuids_to_str(update_data))
    
    updated_user_doc = user_doc_ref.get()
    return User(**updated_user_doc.to_dict())

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
    idempotency_key: UUID4 = Depends(require_idempotency_key)
):
    """
    Creates a new portfolio for the authenticated user.
    Reference: product_spec.md#331-p_1000-portfolio-creation
    """
    # Check for existing portfolio with the same name for the user
    existing_portfolio = db.collection("portfolios").where("userId", "==", current_user.uid).where("name", "==", request.name).limit(1).get()
    if existing_portfolio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"P_E_1103: A portfolio with the name '{request.name}' already exists."
        )

    new_portfolio = portfolio_service.create_portfolio(user_id=current_user.uid, portfolio_data=request)
    return new_portfolio

@router.get("/users/me/portfolios", response_model=List[Portfolio], summary="Retrieve a list of all portfolios for the current user")
async def get_user_portfolios(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieves a summary list of all portfolios owned by the authenticated user.
    Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval
    """
    portfolios = portfolio_service.get_portfolios_by_user(user_id=current_user.uid)
    return portfolios
