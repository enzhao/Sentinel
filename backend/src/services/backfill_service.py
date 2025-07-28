from src.firebase_setup import db
from src.services.market_data_service import alpha_vantage_service

class BackfillService:
    """
    Handles backfilling historical market data for new tickers.
    """

    @staticmethod
    async def is_data_present(ticker: str) -> bool:
        """
        Checks if any historical data exists for a given ticker.
        """
        # We can check for the existence of the ticker document in the marketData collection.
        doc_ref = db.collection('marketData').document(ticker)
        doc = doc_ref.get()
        return doc.exists

    @staticmethod
    async def backfill_historical_data(ticker: str):
        """
        Orchestrates the backfill process for a single ticker.
        """
        print(f"Checking if historical data needs to be backfilled for {ticker}...")
        
        if await BackfillService.is_data_present(ticker):
            print(f"Data for {ticker} is already present. No backfill needed.")
            return

        print(f"No data found for {ticker}. Starting historical data backfill...")
        historical_data = await alpha_vantage_service.get_historical_daily_data(ticker, days=200)

        if not historical_data:
            print(f"Failed to fetch historical data for {ticker}.")
            return

        batch = db.batch()
        for data_point in historical_data:
            date_str = data_point.date.strftime('%Y-%m-%d')
            doc_ref = db.collection('marketData').document(ticker).collection('dailyPrices').document(date_str)
            batch.set(doc_ref, data_point.model_dump())
        
        batch.commit()
        print(f"Successfully backfilled {len(historical_data)} days of data for {ticker}.")

# Instantiate the service
backfill_service = BackfillService()
