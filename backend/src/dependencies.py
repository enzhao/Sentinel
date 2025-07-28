from fastapi import Header, HTTPException, status
from pydantic import UUID4

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
