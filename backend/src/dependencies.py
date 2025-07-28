from fastapi import Header, HTTPException, status

async def require_idempotency_key(idempotency_key: str = Header(..., alias="Idempotency-Key")):
    """
    A dependency that requires the Idempotency-Key header.

    Its primary purpose is to ensure the header is documented in the OpenAPI spec.
    The core logic is handled by the idempotency_middleware, but this provides
    explicit, per-endpoint documentation and an early failure point.
    """
    # The middleware provides the main enforcement. This is a redundant check
    # that also serves as documentation.
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required for this operation."
        )
    return idempotency_key
