import asyncio
import httpx
import sys
import os

# Add the backend directory to the Python path to allow imports from the 'src' module.
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_root)

from src.settings import settings

# --- Configuration ---
API_KEY = settings.ALPHA_VANTAGE_API_KEY
BASE_URL = "https://www.alphavantage.co/query"
TICKER = "GOOGL"
VIX_PROXY_TICKER = "VIXY"

# --- DEPRECATION NOTICE ---
# The Sentinel backend no longer fetches individual technical indicators directly
# from the Alpha Vantage API. Instead, it fetches only the raw daily OHLCV data
# and calculates all required indicators internally using the 'finta' library.
#
# This script has been updated to reflect this change. It now only tests the
# basic API connectivity and the fetching of the TIME_SERIES_DAILY function,
# which is the only function the backend relies on. The previous functions for
# fetching SMA, VWMA, RSI, etc., have been removed as they are obsolete.

async def fetch_alpha_vantage(params: dict):
    """A helper function to make requests to the Alpha Vantage API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            # The free tier has a strict rate limit, check for the note
            if "Note" in data:
                print(f"API Rate Limit Note: {data['Note']}")
            return data
    except httpx.HTTPStatusError as e:
        return {"Error": f"HTTP error occurred: {e}"}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {e}"}

async def get_ohlc(ticker: str):
    """Fetches the latest daily Open, High, Low, Close data."""
    print(f"--- Fetching Daily OHLC for {ticker} ---")
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    data = await fetch_alpha_vantage(params)
    if "Time Series (Daily)" in data:
        latest_date = next(iter(data["Time Series (Daily)"]))
        print("Successfully fetched latest data point:")
        print(data["Time Series (Daily)"][latest_date])
    else:
        print("Failed to fetch data:")
        print(data)

async def main():
    """Runs the updated API test call."""
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE" or API_KEY == "TEST_KEY_DO_NOT_USE":
        print("ERROR: Alpha Vantage API key is not configured.")
        print("Please create a 'backend/.env' file and add your key to it.")
        return

    print("Starting live Alpha Vantage API test for TIME_SERIES_DAILY function...")
    
    await get_ohlc(TICKER)
    
    print("---")
    
    await get_ohlc(VIX_PROXY_TICKER)
    
    print("Test complete.")

if __name__ == "__main__":
    asyncio.run(main())
