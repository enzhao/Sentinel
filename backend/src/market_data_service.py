from typing import Dict, List, Optional
import httpx
from .settings import settings
from .models import MarketDataDB
from datetime import datetime

class AlphaVantageService:
    """
    A service to fetch real market data from the Alpha Vantage API.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    async def get_daily_data(self, ticker: str) -> Optional[MarketDataDB]:
        """
        Fetches the latest daily time series data for a single ticker.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "compact" # We only need the most recent data
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

            if "Error Message" in data or "Time Series (Daily)" not in data:
                print(f"Error fetching data for {ticker}: {data.get('Error Message', 'Invalid format')}")
                return None

            latest_date_str = next(iter(data["Time Series (Daily)"]))
            latest_data = data["Time Series (Daily)"][latest_date_str]

            return MarketDataDB(
                ticker=ticker,
                date=datetime.strptime(latest_date_str, '%Y-%m-%d'),
                open=float(latest_data["1. open"]),
                high=float(latest_data["2. high"]),
                low=float(latest_data["3. low"]),
                close=float(latest_data["4. close"]),
                volume=int(latest_data["5. volume"])
            )
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching data for {ticker}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred for {ticker}: {e}")
            return None

    async def get_historical_daily_data(self, ticker: str, days: int = 200) -> List[MarketDataDB]:
        """
        Fetches the historical daily time series data for a single ticker.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "full" # Fetch the full history
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

            if "Error Message" in data or "Time Series (Daily)" not in data:
                print(f"Error fetching historical data for {ticker}: {data.get('Error Message', 'Invalid format')}")
                return []

            time_series = data["Time Series (Daily)"]
            
            # Convert the data to MarketDataDB objects and limit to the last `days`
            market_data_list = []
            for date_str, daily_data in list(time_series.items())[:days]:
                market_data_list.append(MarketDataDB(
                    ticker=ticker,
                    date=datetime.strptime(date_str, '%Y-%m-%d'),
                    open=float(daily_data["1. open"]),
                    high=float(daily_data["2. high"]),
                    low=float(daily_data["3. low"]),
                    close=float(daily_data["4. close"]),
                    volume=int(daily_data["5. volume"])
                ))
            return market_data_list
        except Exception as e:
            print(f"An unexpected error occurred while fetching historical data for {ticker}: {e}")
            return []


# Instantiate the service with the API key from settings
alpha_vantage_service = AlphaVantageService(api_key=settings.ALPHA_VANTAGE_API_KEY)