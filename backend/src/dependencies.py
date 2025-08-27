import os
from fastapi import Header, HTTPException, status, Depends
from pydantic import UUID4
from firebase_admin import auth
from uuid import UUID

# Use the correct, consistent import
from .firebase_setup import get_db_client
from .core.internal_models import CurrentUser
from .services.user_service import UserService
from .services.portfolio_service import PortfolioService
from .services.idempotency_service import IdempotencyService

def get_db():
    """
    Dependency that provides the Firestore client.
    """
    return get_db_client()

def get_portfolio_service(db_client=Depends(get_db)) -> PortfolioService:
    """
    Dependency that provides a PortfolioService instance.
    """
    return PortfolioService(db_client)

def get_user_service(db_client=Depends(get_db), portfolio_service: PortfolioService = Depends(get_portfolio_service)) -> UserService:
    """
    Dependency that provides a UserService instance.
    """
    return UserService(db_client, portfolio_service)

def get_idempotency_service(db_client=Depends(get_db)) -> IdempotencyService:
    """
    Dependency that provides an IdempotencyService instance.
    """
    return IdempotencyService(db_client)

async def require_idempotency_key(idempotency_key: UUID4 = Header(..., alias="Idempotency-Key")):
    """
    A dependency that requires the Idempotency-Key header to be a valid UUID v4.
    """
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required for this operation."
        )
    return idempotency_key

async def get_current_user(authorization: str = Header(..., alias="Authorization"), db=Depends(get_db)):
    """
    A dependency that verifies the Firebase ID Token from the Authorization header.
    In a test environment, it treats the token as a raw UID.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing."
        )

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization scheme must be Bearer."
            )
        
        # --- THIS IS THE KEY CHANGE ---
        # If we are in a test environment, we treat the token as a simple UID
        # and create a mock "decoded_token" object.
        if os.environ.get("ENV") in ["dev", "test"]:
            uid = token
            # Create a mock token that has the same structure as a real one
            decoded_token = {
                'uid': uid,
                'email': f'{uid}@example.com' 
            }
        else:
            # In production, verify the actual JWT from the client
            decoded_token = auth.verify_id_token(token)
        # --- END OF CHANGE ---
        
        user_doc_ref = db.collection("users").document(decoded_token["uid"])
        user_doc = user_doc_ref.get()

        default_portfolio_id = None
        if user_doc.exists:
            user_data = user_doc.to_dict()
            default_portfolio_id = user_data.get("defaultPortfolioId")
            if default_portfolio_id:
                default_portfolio_id = UUID(default_portfolio_id)

        return CurrentUser(
            uid=decoded_token["uid"],
            email=decoded_token["email"],
            username=decoded_token.get("name", decoded_token["email"]),
            defaultPortfolioId=default_portfolio_id
        )

    except (ValueError, auth.InvalidIdTokenError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during authentication: {e}"
        )
