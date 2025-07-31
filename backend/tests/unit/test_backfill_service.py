import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.services.backfill_service import BackfillService
from src.models import MarketDataDB
from datetime import datetime

@pytest.mark.asyncio
async def test_is_data_present_when_exists():
    """
    Tests that is_data_present returns True when the 'daily' subcollection has documents.
    """
    # Mock the stream to return a generator with one mock document
    mock_stream = MagicMock()
    mock_stream.return_value = (i for i in [MagicMock()])

    with patch('src.firebase_setup.db.collection') as mock_collection:
        mock_collection.return_value.document.return_value.collection.return_value.limit.return_value.stream = mock_stream
        
        assert await BackfillService.is_data_present("AAPL") is True

@pytest.mark.asyncio
async def test_is_data_present_when_not_exists():
    """
    Tests that is_data_present returns False when the 'daily' subcollection is empty.
    """
    # Mock the stream to return an empty generator
    mock_stream = MagicMock()
    mock_stream.return_value = (i for i in [])

    with patch('src.firebase_setup.db.collection') as mock_collection:
        mock_collection.return_value.document.return_value.collection.return_value.limit.return_value.stream = mock_stream
        
        assert await BackfillService.is_data_present("UNKNOWN") is False

@pytest.mark.asyncio
async def test_backfill_does_not_run_if_data_present():
    """
    Tests that the backfill process does NOT call the external API if data is already present.
    """
    with patch('src.services.backfill_service.BackfillService.is_data_present', new_callable=AsyncMock, return_value=True):
        with patch('src.services.market_data_service.alpha_vantage_service.get_historical_daily_data', new_callable=AsyncMock) as mock_fetch:
            
            await BackfillService.backfill_historical_data("AAPL")
            
            mock_fetch.assert_not_called()

@pytest.mark.asyncio
async def test_backfill_fetches_and_saves_data():
    """
    Tests the full backfill happy path: data is missing, so it's fetched and saved.
    """
    # 1. Mock the data that will be "returned" by the external API
    mock_historical_data = [
        MarketDataDB(ticker="TSLA", date=datetime.now(), open=1, high=2, low=3, close=180.0, volume=100),
        MarketDataDB(ticker="TSLA", date=datetime.now(), open=2, high=3, low=4, close=181.0, volume=200)
    ]

    # 2. Set up the patches
    with patch('src.services.backfill_service.BackfillService.is_data_present', new_callable=AsyncMock, return_value=False):
        with patch('src.services.market_data_service.alpha_vantage_service.get_historical_daily_data', new_callable=AsyncMock, return_value=mock_historical_data) as mock_fetch:
            with patch('src.firebase_setup.db.batch') as mock_batch:
                mock_set = MagicMock()
                mock_batch.return_value.set = mock_set
                mock_commit = MagicMock()
                mock_batch.return_value.commit = mock_commit

                # 3. Run the service
                await BackfillService.backfill_historical_data("TSLA")

                # 4. Assertions
                mock_fetch.assert_awaited_once_with("TSLA", days=200)
                assert mock_set.call_count == 2
                mock_commit.assert_called_once()
