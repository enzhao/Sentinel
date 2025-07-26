from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth

# This scheme tells FastAPI to look for a token in the "Authorization: Bearer <token>" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to verify Firebase ID token and return user data.
    """
    try:
        # Verify the token against the Firebase Auth API.
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        # If the token is invalid for any reason, raise an HTTP 401 Unauthorized error.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
