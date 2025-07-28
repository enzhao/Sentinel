import asyncio
import sys
import os
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# --- Real Service Imports ---
# This script uses the actual services, not mocks.
from backend.src.market_data_service import alpha_vantage_service
from backend.src.firebase_setup import db
from backend.src.settings import settings

# --- Configuration ---
TEST_TICKER = "IBM"  # Use a common, stable ticker for testing

async def run_e2e_test():
    """
    Performs a full end-to-end test of the data pipeline:
    1. Fetches real data from Alpha Vantage.
    2. Writes it to the live Firestore database.
    3. Reads it back from Firestore.
    4. Asserts the data is correct.
    5. Cleans up the created data.
    """
    print("--- Starting E2E Data Pipeline Test ---")

    # 1. Check for credentials
    if not settings.ALPHA_VANTAGE_API_KEY or settings.ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ ERROR: Live Alpha Vantage API key is not configured in backend/.env")
        return

    print(f"1. Fetching real market data for ticker: {TEST_TICKER}...")
    
    # 2. Fetch real data from Alpha Vantage
    fetched_data = await alpha_vantage_service.get_daily_data(TEST_TICKER)
    
    assert fetched_data is not None, "Failed to fetch data from Alpha Vantage."
    assert fetched_data.ticker == TEST_TICKER
    assert fetched_data.close > 0
    
    print(f"   ✅ Fetched closing price: {fetched_data.close}")

    # 3. Write the fetched data to Firestore
    date_str = fetched_data.date.strftime('%Y-%m-%d')
    doc_ref = db.collection('marketData').document(TEST_TICKER).collection('dailyPrices').document(date_str)
    
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