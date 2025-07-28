from typing import Dict, List, Optional
import httpx
from src.settings import settings
from src.models import MarketDataDB
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
            "outputsize": "compact"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = await response.json()

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
            "outputsize": "full"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = await response.json()

            if "Error Message" in data or "Time Series (Daily)" not in data:
                print(f"Error fetching historical data for {ticker}: {data.get('Error Message', 'Invalid format')}")
                return []

            time_series = data["Time Series (Daily)"]
            
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

    async def get_ma200(self, ticker: str) -> Optional[float]:
        """Fetches the 200-day simple moving average."""
        params = {"function": "SMA", "symbol": ticker, "interval": "daily", "time_period": "200", "series_type": "close", "apikey": self.api_key}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = await response.json()
            if "Technical Analysis: SMA" in data:
                latest_date = next(iter(data["Technical Analysis: SMA"]))
                return float(data["Technical Analysis: SMA"][latest_date]["SMA"])
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching MA200 for {ticker}: {e}")
            return None

    async def get_weekly_rsi(self, ticker: str) -> Optional[float]:
        """Fetches the weekly Relative Strength Index."""
        params = {"function": "RSI", "symbol": ticker, "interval": "weekly", "time_period": "14", "series_type": "close", "apikey": self.api_key}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = await response.json()
            if "Technical Analysis: RSI" in data:
                latest_date = next(iter(data["Technical Analysis: RSI"]))
                return float(data["Technical Analysis: RSI"][latest_date]["RSI"])
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching Weekly RSI for {ticker}: {e}")
            return None

    async def get_atr(self, ticker: str) -> Optional[float]:
        """Fetches the latest Average True Range (ATR) for a single ticker."""
        params = {"function": "ATR", "symbol": ticker, "interval": "daily", "time_period": "14", "apikey": self.api_key}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = await response.json()
            if "Technical Analysis: ATR" in data:
                latest_date = next(iter(data["Technical Analysis: ATR"]))
                return float(data["Technical Analysis: ATR"][latest_date]["ATR"])
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching ATR for {ticker}: {e}")
            return None

# Instantiate the service with the API key from settings
alpha_vantage_service = AlphaVantageService(api_key=settings.ALPHA_VANTAGE_API_KEY)
