import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.market_data_service import AlphaVantageService
from src.models import MarketDataDB
from datetime import datetime

# Initialize the service with a dummy key for testing
service = AlphaVantageService(api_key="TEST_KEY")

# Your brilliant helper function to create a mock that can be awaited
# and has an awaitable .json() method.
def create_mock_async_get(json_response):
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock()  #  fix here: make it regular, not async
    mock_response.json = AsyncMock(return_value=json_response)
    return AsyncMock(return_value=mock_response)

@pytest.mark.asyncio
async def test_get_daily_data_success():
    """Tests successful fetching of daily OHLC data."""
    api_response = {
        "Time Series (Daily)": {
            "2025-07-28": {"1. open": "150.0", "2. high": "155.0", "3. low": "149.0", "4. close": "154.5", "5. volume": "100000"}
        }
    }
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_daily_data("IBM")
        assert isinstance(result, MarketDataDB)
        assert result.ticker == "IBM"
        assert result.close == 154.5

@pytest.mark.asyncio
async def test_get_daily_data_api_error():
    """Tests handling of an API error message from Alpha Vantage."""
    api_response = {"Error Message": "Invalid API call."}
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_daily_data("INVALID")
        assert result is None

@pytest.mark.asyncio
async def test_get_ma200_success():
    """Tests successful fetching of the 200-day moving average."""
    api_response = {"Technical Analysis: SMA": {"2025-07-28": {"SMA": "175.50"}}}
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_ma200("IBM")
        assert result == 175.50

@pytest.mark.asyncio
async def test_get_weekly_rsi_success():
    """Tests successful fetching of the weekly RSI."""
    api_response = {"Technical Analysis: RSI": {"2025-07-28": {"RSI": "65.75"}}}
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_weekly_rsi("IBM")
        assert result == 65.75

@pytest.mark.asyncio
async def test_get_atr_success():
    """Tests successful fetching of the ATR."""
    api_response = {"Technical Analysis: ATR": {"2025-07-28": {"ATR": "12.34"}}}
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        result = await service.get_atr("IBM")
        assert result == 12.34

@pytest.mark.asyncio
async def test_get_historical_data_success():
    """Tests successful fetching of historical daily data."""
    api_response = {
        "Time Series (Daily)": {
            "2025-07-28": {"1. open": "150.0", "2. high": "155.0", "3. low": "149.0", "4. close": "154.5", "5. volume": "100000"},
            "2025-07-27": {"1. open": "148.0", "2. high": "152.0", "3. low": "147.0", "4. close": "150.0", "5. volume": "120000"}
        }
    }
    with patch('httpx.AsyncClient.get', new=create_mock_async_get(api_response)):
        results = await service.get_historical_daily_data("IBM", days=2)
        assert len(results) == 2
        assert isinstance(results[0], MarketDataDB)
        assert results[0].close == 154.5