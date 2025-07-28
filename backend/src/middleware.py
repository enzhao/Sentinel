import json
from fastapi import Request, status
from fastapi.responses import JSONResponse
from firebase_admin import auth

from .idempotency_service import idempotency_service

async def idempotency_middleware(request: Request, call_next):
    # Only apply to state-changing methods
    if request.method not in ["POST", "PUT", "DELETE"]:
        return await call_next(request)

    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Idempotency-Key header is required for this operation."},
        )

    # --- User Verification ---
    # This is a crucial step to scope the idempotency key to the user
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header is missing."},
            )
        # Verify the token to get the user's UID
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"Invalid authentication credentials: {e}"},
        )
    # --- End User Verification ---

    # 1. Check for a stored response
    stored_response_data = idempotency_service.get_idempotent_response(idempotency_key, user_id)
    if stored_response_data:
        # If found, return the stored response immediately
        return JSONResponse(
            status_code=stored_response_data["status_code"],
            content=json.loads(stored_response_data["body"]),
        )

    # 2. If no stored response, proceed with the actual endpoint
    response = await call_next(request)

    # 3. Store the new response before returning it
    # A response body can only be read once, so we need to handle it carefully
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    
    response_data_to_store = {
        "status_code": response.status_code,
        "body": response_body.decode(),
    }
    idempotency_service.store_idempotent_response(idempotency_key, user_id, response_data_to_store)

    # We need to construct a new response because the body of the original
    # has been consumed by the iterator.
    return JSONResponse(
        status_code=response.status_code,
        content=json.loads(response_body.decode()) if response_body else None,
        headers=dict(response.headers),
    )
