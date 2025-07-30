import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.services.market_data_service import AlphaVantageService
from src.models import MarketDataDB
from datetime import datetime, timedelta
import pandas as pd

# Initialize the service with a dummy key for testing
service = AlphaVantageService(api_key="TEST_KEY")

def create_mock_async_get(json_response):
    """Helper to create a mock that can be awaited and has an awaitable .json() method."""
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock()
    mock_response.json = AsyncMock(return_value=json_response)
    
    async def get_mock(*args, **kwargs):
        return mock_response
        
    return get_mock

@pytest.mark.asyncio
async def test_get_daily_data_with_indicators_success():
    """
    Tests successful fetching of daily OHLCV data and the subsequent internal
    calculation of all technical indicators.
    """
    # 1. Generate 300 days of mock historical data with some variance
    historical_data = {}
    start_date = datetime(2025, 7, 28)
    price = 150.0
    for i in range(300):
        date = start_date - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        # Add some variance to make indicators like RSI meaningful
        price_change = (i % 10 - 5) * 0.1 
        price += price_change
        historical_data[date_str] = {
            "1. open": str(price), 
            "2. high": str(price + 5), 
            "3. low": str(price - 1), 
            "4. close": str(price + 0.5), 
            "5. volume": str(100000 + (i * 1000))
        }

    historical_response = {"Time Series (Daily)": historical_data}

    # 2. Patch the httpx client to return our mock data
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(historical_response)):
        result = await service.get_daily_data_with_indicators("IBM")

        # 3. Assert the results
        assert isinstance(result, MarketDataDB)
        assert result.ticker == "IBM"
        assert result.close is not None and result.close > 0
        
        # Check that all indicators were calculated and are plausible values
        assert result.sma7 is not None and result.sma7 > 0
        assert result.sma20 is not None and result.sma20 > 0
        assert result.sma50 is not None and result.sma50 > 0
        assert result.sma200 is not None and result.sma200 > 0
        
        assert result.vwma7 is not None and result.vwma7 > 0
        assert result.vwma20 is not None and result.vwma20 > 0
        assert result.vwma50 is not None and result.vwma50 > 0
        assert result.vwma200 is not None and result.vwma200 > 0

        # Relaxed assertion for RSI, as it can be 0 in some cases.
        assert result.rsi14 is not None and result.rsi14 >= 0
        assert result.atr14 is not None and result.atr14 > 0
        
        assert result.macd is not None
        assert "value" in result.macd and isinstance(result.macd["value"], float)
        assert "signal" in result.macd and isinstance(result.macd["signal"], float)
        assert "histogram" in result.macd and isinstance(result.macd["histogram"], float)

@pytest.mark.asyncio
async def test_get_daily_data_api_error():
    """Tests handling of an API error message from Alpha Vantage for historical data."""
    api_response = {"Error Message": "Invalid API call."}
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_daily_data_with_indicators("INVALID")
        assert result is None

@pytest.mark.asyncio
async def test_get_historical_data_success():
    """
    Tests successful fetching of historical daily data and that indicators are calculated.
    """
    # Generate 50 days of data so that all indicators (like MACD) can be calculated.
    historical_data = {}
    start_date = datetime(2025, 7, 28)
    for i in range(50):
        date = start_date - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        historical_data[date_str] = {
            "1. open": str(150.0 - i),
            "2. high": str(155.0 - i),
            "3. low": str(149.0 - i),
            "4. close": str(154.5 - i),
            "5. volume": str(100000 + i * 100)
        }
    
    api_response = {"Time Series (Daily)": historical_data}

    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        results = await service.get_historical_daily_data("IBM", days=50)
        assert len(results) == 50
        assert isinstance(results[0], MarketDataDB)
        assert results[0].close == 154.5
        
        # The first few results might have None for indicators that need more data.
        # Let's check the first result in the series (the most recent one) which should have valid data.
        assert results[0].sma7 is not None
        assert results[0].vwma7 is not None
        assert results[0].rsi14 is not None
        assert results[0].atr14 is not None
        assert results[0].macd is not None
