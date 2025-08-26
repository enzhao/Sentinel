from fastapi import Header, HTTPException, status
from pydantic import UUID4
from firebase_admin import auth
from firebase_setup import initialize_firebase_app, db
from .core.internal_models import CurrentUser

async def require_idempotency_key(idempotency_key: UUID4 = Header(..., alias="Idempotency-Key")):
    """
    A dependency that requires the Idempotency-Key header to be a valid UUID v4.

    Its primary purpose is to ensure the header is documented in the OpenAPI spec
    and that its format is validated upon arrival.
    """
    if not idempotency_key:
        # This case is largely handled by FastAPI's header validation,
        # but remains for clarity.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required for this operation."
        )
    return idempotency_key

async def get_current_user(authorization: str = Header(..., alias="Authorization")):
    """
    A dependency that verifies the Firebase ID Token from the Authorization header.
    Returns the decoded token if valid, otherwise raises an HTTPException.
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
        
        # Ensure Firebase app is initialized before verifying token
        initialize_firebase_app()
        
        decoded_token = auth.verify_id_token(token)
        
        user_doc_ref = db.collection("users").document(decoded_token["uid"])
        user_doc = user_doc_ref.get()

        default_portfolio_id = None
        if user_doc.exists:
            user_data = user_doc.to_dict()
            default_portfolio_id = user_data.get("defaultPortfolioId")
            if default_portfolio_id:
                from uuid import UUID
                default_portfolio_id = UUID(default_portfolio_id)

        return CurrentUser(
            uid=decoded_token["uid"],
            email=decoded_token["email"],
            username=decoded_token.get("name", decoded_token["email"]),
            defaultPortfolioId=default_portfolio_id
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token malformed or invalid."
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided ID token is invalid."
        )
    except Exception as e:
        # Catch any other unexpected errors during token verification
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {e}"
        )
