import asyncio
import sys
import os
from datetime import datetime

# Set the environment to 'local' BEFORE importing any project modules
# This ensures that firebase_setup.py uses the service account key.
os.environ['ENV'] = 'local'

# Add the backend directory to the Python path
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_root)

# --- Real Service Imports ---
# This script uses the actual services, not mocks.
from src.services.market_data_service import alpha_vantage_service
from src.firebase_setup import db
from src.settings import settings

# --- Configuration ---
TEST_TICKER = "IBM"  # Use a common, stable ticker for testing

async def run_e2e_test():
    """
    Performs a full end-to-end test of the data pipeline:
    1. Fetches real data and all indicators from Alpha Vantage.
    2. Writes the consolidated data to the live Firestore database.
    3. Reads it back from Firestore.
    4. Asserts the data is correct, including new fields.
    5. Cleans up the created data.
    """
    print("--- Starting E2E Data Pipeline Test ---")

    # 1. Check for credentials
    if not settings.ALPHA_VANTAGE_API_KEY or settings.ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ ERROR: Live Alpha Vantage API key is not configured in backend/.env")
        return

    print(f"1. Fetching real market data and all indicators for ticker: {TEST_TICKER}...")
    
    # 2. Fetch real data using the consolidated service function
    fetched_data = await alpha_vantage_service.get_daily_data_with_indicators(TEST_TICKER)
    
    assert fetched_data is not None, "Failed to fetch data from Alpha Vantage."
    assert fetched_data.ticker == TEST_TICKER
    assert fetched_data.close > 0
    assert fetched_data.sma200 is not None and fetched_data.sma200 > 0
    assert fetched_data.rsi14 is not None and fetched_data.rsi14 > 0
    assert fetched_data.vwma200 is not None and fetched_data.vwma200 > 0
    assert fetched_data.macd is not None
    assert "value" in fetched_data.macd and "signal" in fetched_data.macd and "histogram" in fetched_data.macd

    print(f"   ✅ Fetched closing price: {fetched_data.close}")
    print(f"   ✅ Fetched SMA200: {fetched_data.sma200}")
    print(f"   ✅ Fetched VWMA200: {fetched_data.vwma200}")
    print(f"   ✅ Fetched MACD: {fetched_data.macd}")


    # 3. Write the fetched data to Firestore
    date_str = fetched_data.date.strftime('%Y-%m-%d')
    # The path has changed to /marketData/{ticker}/daily/{date}
    doc_ref = db.collection('marketData').document(TEST_TICKER).collection('daily').document(date_str)
    
    print(f"2. Writing data to Firestore at path: {doc_ref.path}...")
    doc_ref.set(fetched_data.model_dump())
    print("   ✅ Write successful.")

    # 4. Read the data back from Firestore
    print("3. Reading data back from Firestore...")
    doc = doc_ref.get()
    assert doc.exists, "Data was not found in Firestore after writing."
    
    read_data = doc.to_dict()
    print("   ✅ Read successful.")

    # 5. Assert that the written and read data match
    print("4. Verifying data integrity...")
    assert read_data["ticker"] == fetched_data.ticker
    assert read_data["close"] == fetched_data.close
    assert read_data["sma200"] == fetched_data.sma200
    assert read_data["rsi14"] == fetched_data.rsi14
    assert read_data["vwma200"] == fetched_data.vwma200
    assert read_data["macd"]["value"] == fetched_data.macd["value"]
    assert read_data["macd"]["signal"] == fetched_data.macd["signal"]
    assert read_data["macd"]["histogram"] == fetched_data.macd["histogram"]
    print("   ✅ Data is consistent.")

    # 6. Clean up the created data
    print(f"5. Cleaning up test data from Firestore...")
    doc_ref.delete()
    
    # Verify deletion
    doc_after_delete = doc_ref.get()
    assert not doc_after_delete.exists, "Cleanup failed: Test data was not deleted."
    print("   ✅ Cleanup successful.")

    print("\n--- ✅ E2E Data Pipeline Test Passed Successfully! ---")


if __name__ == "__main__":
    asyncio.run(run_e2e_test())