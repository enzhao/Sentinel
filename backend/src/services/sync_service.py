import asyncio
from src.firebase_setup import db
from src.services.market_data_service import alpha_vantage_service
from src.models import MarketDataDB

VIX_PROXY_TICKER = "VIXY"

class SyncService:
    """
    Handles the daily synchronization of market data.
    """

    @staticmethod
    async def get_all_unique_tickers() -> set[str]:
        """
        Scans the 'portfolios' collection in Firestore to find all unique tickers
        across all user holdings, and always includes the VIX proxy ticker.
        """
        unique_tickers = set()
        portfolios_stream = db.collection('portfolios').stream()

        # Using async for to iterate over the async generator
        async for portfolio in portfolios_stream:
            holdings = portfolio.to_dict().get('holdings', [])
            for holding in holdings:
                if 'ticker' in holding:
                    unique_tickers.add(holding['ticker'])
        
        # Always include the VIX proxy ticker in the daily sync
        unique_tickers.add(VIX_PROXY_TICKER)
        
        print(f"Found {len(unique_tickers)} unique tickers to sync.")
        return unique_tickers

    @staticmethod
    async def sync_market_data():
        """
        The main cron job function. It gets all unique tickers, fetches their
        latest daily data and all technical indicators in a single call per ticker,
        and stores it in Firestore.
        """
        tickers = await SyncService.get_all_unique_tickers()
        if not tickers:
            print("No tickers to sync. Exiting.")
            return

        # Create a list of tasks to fetch all data for each ticker in parallel
        tasks = [alpha_vantage_service.get_daily_data_with_indicators(ticker) for ticker in tickers]
        
        results = await asyncio.gather(*tasks)
        
        # Filter out any None results from failed API calls
        fetched_data: list[MarketDataDB] = [res for res in results if res is not None]

        if not fetched_data:
            print("No market data fetched. Nothing to save.")
            return

        batch = db.batch()
        for data in fetched_data:
            # The document ID is now the date string, under a specific ticker document
            date_str = data.date.strftime('%Y-%m-%d')
            doc_ref = db.collection('marketData').document(data.ticker).collection('daily').document(date_str)
            batch.set(doc_ref, data.model_dump())
        
        batch.commit()
        print(f"Successfully synced and stored market data for {len(fetched_data)} tickers.")

# Instantiate the service
sync_service = SyncService()
