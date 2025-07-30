from typing import List, Optional
import httpx
from src.settings import settings
from src.models import MarketDataDB
from datetime import datetime
import pandas as pd
from finta import TA

class AlphaVantageService:
    """
    A service to fetch raw market data from the Alpha Vantage API and
    calculate all technical indicators internally using finta.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def _calculate_historical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates all required technical indicators for a historical DataFrame using finta.
        Finta expects OHLC columns to be lowercase, which they are.
        """
        # Finta calculates indicators and appends them to the DataFrame.
        # The DataFrame should be sorted with the oldest date first.
        df_finta = df.copy()
        df_finta = df_finta.iloc[::-1] # Oldest first

        # Calculate all indicators
        df_finta['sma7'] = TA.SMA(df_finta, period=7)
        df_finta['sma20'] = TA.SMA(df_finta, period=20)
        df_finta['sma50'] = TA.SMA(df_finta, period=50)
        df_finta['sma200'] = TA.SMA(df_finta, period=200)
        
        # Manual implementation for VWMA
        for period in [7, 20, 50, 200]:
            cv = df_finta['close'] * df_finta['volume']
            df_finta[f'vwma{period}'] = cv.rolling(window=period).sum() / df_finta['volume'].rolling(window=period).sum()

        df_finta['rsi14'] = TA.RSI(df_finta, period=14)
        df_finta['atr14'] = TA.ATR(df_finta, period=14)
        
        # Finta's MACD returns a DataFrame with MACD, SIGNAL, and HISTOGRAM
        macd_df = TA.MACD(df_finta)
        df_finta['macd_value'] = macd_df['MACD']
        df_finta['macd_signal'] = macd_df['SIGNAL']
        df_finta['macd_histogram'] = macd_df['MACD'] - macd_df['SIGNAL']

        # Return in descending order (newest first)
        return df_finta.iloc[::-1]

    async def get_daily_data_with_indicators(self, ticker: str) -> Optional[MarketDataDB]:
        """
        Fetches the latest daily time series data with all indicators calculated.
        """
        # We get the full historical data and just return the first (most recent) entry.
        historical_data = await self.get_historical_daily_data(ticker, days=300)
        if not historical_data:
            return None
        return historical_data[0]

    async def get_historical_daily_data(self, ticker: str, days: int = 300) -> List[MarketDataDB]:
        """
        Fetches the historical daily time series data for a single ticker,
        calculates all technical indicators for the entire history, and returns it.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "full" # Always get full data for accurate calculations
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

            if "Error Message" in data or "Time Series (Daily)" not in data:
                # This handles API-specific errors, like an invalid ticker
                print(f"Error fetching historical data for {ticker}: {data.get('Error Message', 'Invalid format')}")
                return []

            time_series = data["Time Series (Daily)"]
            
            # Convert raw data to a list of dictionaries
            raw_data_list = []
            for date_str, daily_data in time_series.items():
                raw_data_list.append({
                    "date": datetime.strptime(date_str, '%Y-%m-%d'),
                    "ticker": ticker,
                    "open": float(daily_data["1. open"]),
                    "high": float(daily_data["2. high"]),
                    "low": float(daily_data["3. low"]),
                    "close": float(daily_data["4. close"]),
                    "volume": int(daily_data["5. volume"])
                })

            # Create a DataFrame and calculate indicators for the whole history
            df = pd.DataFrame(raw_data_list)
            df_with_indicators = self._calculate_historical_indicators(df)

            # Limit to the number of days requested
            df_with_indicators = df_with_indicators.head(days)

            # Convert DataFrame back to a list of MarketDataDB objects
            market_data_list = []
            for _, row in df_with_indicators.iterrows():
                row_dict = row.to_dict()
                # Handle NaN values from indicator calculations for fields that are Optional
                for key, value in row_dict.items():
                    if pd.isna(value):
                        row_dict[key] = None

                # Special handling for MACD object
                macd_data = None
                if row_dict.get("macd_value") is not None:
                    macd_data = {
                        "value": row_dict.get("macd_value"),
                        "signal": row_dict.get("macd_signal"),
                        "histogram": row_dict.get("macd_histogram"),
                    }
                
                market_data_list.append(MarketDataDB(
                    ticker=row_dict["ticker"],
                    date=row_dict["date"],
                    open=row_dict["open"],
                    high=row_dict["high"],
                    low=row_dict["low"],
                    close=row_dict["close"],
                    volume=row_dict["volume"],
                    sma7=row_dict.get("sma7"),
                    sma20=row_dict.get("sma20"),
                    sma50=row_dict.get("sma50"),
                    sma200=row_dict.get("sma200"),
                    vwma7=row_dict.get("vwma7"),
                    vwma20=row_dict.get("vwma20"),
                    vwma50=row_dict.get("vwma50"),
                    vwma200=row_dict.get("vwma200"),
                    rsi14=row_dict.get("rsi14"),
                    atr14=row_dict.get("atr14"),
                    macd=macd_data
                ))
            return market_data_list
        except httpx.HTTPStatusError as e:
            # This handles network-level errors (e.g., 4xx, 5xx responses)
            print(f"HTTP error occurred while fetching data for {ticker}: {e}")
            return []
        except Exception as e:
            # This catches other unexpected errors (e.g., parsing, calculation)
            print(f"An unexpected error occurred while processing data for {ticker}: {e}")
            return []

# Instantiate the service with the API key from settings
alpha_vantage_service = AlphaVantageService(api_key=settings.ALPHA_VANTAGE_API_KEY)
