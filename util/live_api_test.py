import asyncio
import httpx
import sys
import os

# This is the key change: Add the project root to the Python path
# to allow imports from the 'backend' module.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.src.settings import settings

# --- Configuration ---
API_KEY = settings.ALPHA_VANTAGE_API_KEY
BASE_URL = "https://www.alphavantage.co/query"
TICKER = "GOOGL"
VIX_PROXY_TICKER = "VIXY"

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
        print(data["Time Series (Daily)"][latest_date])
    else:
        print(data)

async def get_ma200(ticker: str):
    """Fetches the 200-day simple moving average."""
    print(f"\n--- Fetching 200-Day Moving Average (MA200) for {ticker} ---")
    params = {
        "function": "SMA",
        "symbol": ticker,
        "interval": "daily",
        "time_period": "200",
        "series_type": "close",
        "apikey": API_KEY
    }
    data = await fetch_alpha_vantage(params)
    if "Technical Analysis: SMA" in data:
        latest_date = next(iter(data["Technical Analysis: SMA"]))
        print(data["Technical Analysis: SMA"][latest_date])
    else:
        print(data)

async def get_weekly_rsi(ticker: str):
    """Fetches the weekly Relative Strength Index."""
    print(f"\n--- Fetching Weekly RSI for {ticker} ---")
    params = {
        "function": "RSI",
        "symbol": ticker,
        "interval": "weekly",
        "time_period": "14", # Standard RSI period
        "series_type": "close",
        "apikey": API_KEY
    }
    data = await fetch_alpha_vantage(params)
    if "Technical Analysis: RSI" in data:
        latest_date = next(iter(data["Technical Analysis: RSI"]))
        print(data["Technical Analysis: RSI"][latest_date])
    else:
        print(data)

async def get_atr(ticker: str):
    """Fetches the Average True Range (ATR) technical indicator."""
    print(f"\n--- Fetching Daily ATR for {ticker} ---")
    params = {
        "function": "ATR",
        "symbol": ticker,
        "interval": "daily",
        "time_period": "14", # Standard ATR period
        "apikey": API_KEY
    }
    data = await fetch_alpha_vantage(params)
    if "Technical Analysis: ATR" in data:
        latest_date = next(iter(data["Technical Analysis: ATR"]))
        print(data["Technical Analysis: ATR"][latest_date])
    else:
        print(data)

async def main():
    """Runs all the API test calls."""
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE" or API_KEY == "TEST_KEY_DO_NOT_USE":
        print("ERROR: Alpha Vantage API key is not configured.")
        print("Please create a 'backend/.env' file and add your key to it.")
        return

    print("Starting live Alpha Vantage API test...")
    
    # We need to add a delay between calls to respect the free tier rate limit
    # which is often around 5 calls per minute.
    
    await get_ohlc(TICKER)
    await asyncio.sleep(15) # Wait 15 seconds
    
    await get_ma200(TICKER)
    await asyncio.sleep(15)
    
    await get_weekly_rsi(TICKER)
    await asyncio.sleep(15)
    
    await get_atr(TICKER)
    await asyncio.sleep(15)
    
    await get_ohlc(VIX_PROXY_TICKER)
    
    print("\nTest complete.")

if __name__ == "__main__":
    asyncio.run(main())