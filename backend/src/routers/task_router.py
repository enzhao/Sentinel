from fastapi import APIRouter, Depends, HTTPException, status
from src.auth import get_current_user
from src.services.sync_service import sync_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)] # Protect the endpoint
)

@router.post("/run-daily-market-sync", status_code=status.HTTP_200_OK)
async def run_daily_market_sync():
    """
    Manually triggers the daily market data synchronization job.
    
    In production, this endpoint would be called by a scheduled service like
    Google Cloud Scheduler.
    """
    try:
        await sync_service.sync_market_data()
        return {"message": "Market data synchronization job completed successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during market data sync: {e}"
        )
