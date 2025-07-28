import asyncio
from .firebase_setup import db
from .market_data_service import alpha_vantage_service

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
        latest daily data and all technical indicators, and stores it in Firestore.
        """
        tickers = await SyncService.get_all_unique_tickers()
        if not tickers:
            print("No tickers to sync. Exiting.")
            return

        # Create a list of tasks for all API calls to run in parallel
        tasks = []
        ticker_list = list(tickers)
        for ticker in ticker_list:
            tasks.append(alpha_vantage_service.get_daily_data(ticker))
            tasks.append(alpha_vantage_service.get_ma200(ticker))
            tasks.append(alpha_vantage_service.get_weekly_rsi(ticker))
            tasks.append(alpha_vantage_service.get_atr(ticker))
        
        results = await asyncio.gather(*tasks)
        
        # Process the results, grouping them by ticker
        data_by_ticker = {}
        for i, ticker in enumerate(ticker_list):
            daily_data = results[i*4]
            if daily_data:
                daily_data.ma200 = results[i*4 + 1]
                daily_data.rsi_weekly = results[i*4 + 2]
                daily_data.atr = results[i*4 + 3]
                data_by_ticker[ticker] = daily_data

        if not data_by_ticker:
            print("No market data fetched. Nothing to save.")
            return

        batch = db.batch()
        for ticker, data in data_by_ticker.items():
            date_str = data.date.strftime('%Y-%m-%d')
            doc_ref = db.collection('marketData').document(ticker).collection('dailyPrices').document(date_str)
            batch.set(doc_ref, data.model_dump())
        
        batch.commit()
        print(f"Successfully synced and stored market data for {len(data_by_ticker)} tickers.")

# Instantiate the service
sync_service = SyncService()