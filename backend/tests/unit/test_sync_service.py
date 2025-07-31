import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.services.sync_service import SyncService
from src.models import PortfolioDB, HoldingDB, MarketDataDB
from datetime import datetime

@pytest.mark.asyncio
async def test_get_all_unique_tickers():
    """
    Tests that the service correctly finds all unique tickers from portfolios
    and always includes the VIXY proxy.
    """
    # Mock the database stream
    mock_portfolio_1 = PortfolioDB(userId="u1", name="p1", holdings=[HoldingDB(ticker="AAPL"), HoldingDB(ticker="GOOGL")]).model_dump()
    mock_portfolio_2 = PortfolioDB(userId="u2", name="p2", holdings=[HoldingDB(ticker="MSFT"), HoldingDB(ticker="AAPL")]).model_dump()
    
    mock_doc_1 = MagicMock()
    mock_doc_1.to_dict.return_value = mock_portfolio_1
    mock_doc_2 = MagicMock()
    mock_doc_2.to_dict.return_value = mock_portfolio_2

    class AsyncIterator:
        def __init__(self, items): self.items = items; self.iter = iter(self.items)
        def __aiter__(self): return self
        async def __anext__(self):
            try: return next(self.iter)
            except StopIteration: raise StopAsyncIteration

    with patch('src.firebase_setup.db.collection') as mock_collection:
        mock_collection.return_value.stream.return_value = AsyncIterator([mock_doc_1, mock_doc_2])
        
        tickers = await SyncService.get_all_unique_tickers()
        
        assert tickers == {"AAPL", "GOOGL", "MSFT", "VIXY"}

@pytest.mark.asyncio
async def test_sync_market_data_with_all_indicators():
    """
    Tests the main sync logic, ensuring the consolidated data fetching call
    is used and the complete, correct data is saved to Firestore.
    """
    mock_tickers = {"AAPL", "VIXY"}
    
    # Mock the fully populated MarketDataDB object that the service will return
    mock_aapl_data = MarketDataDB(
        ticker="AAPL",
        date=datetime.now(),
        open=150.0, high=155.0, low=149.0, close=154.5, volume=100000,
        sma200=175.5, sma50=160.1, sma20=155.2, sma7=153.8,
        vwma200=176.2, vwma50=161.5, vwma20=156.3, vwma7=154.1,
        rsi14=65.75,
        atr14=12.34
    )
    # Mock a None response for one of the tickers to simulate a failed API call
    mock_vixy_data = None

    # The service now calls get_daily_data_with_indicators once per ticker.
    # We use side_effect to return different values for different tickers.
    async def get_data_side_effect(ticker):
        if ticker == "AAPL":
            return mock_aapl_data
        else:
            return mock_vixy_data

    with patch('src.services.sync_service.SyncService.get_all_unique_tickers', new_callable=AsyncMock, return_value=mock_tickers):
        with patch('src.services.market_data_service.alpha_vantage_service.get_daily_data_with_indicators', side_effect=get_data_side_effect) as mock_fetch:
            
            with patch('src.firebase_setup.db.batch') as mock_batch:
                mock_set = MagicMock()
                mock_batch.return_value.set = mock_set
                mock_commit = MagicMock()
                mock_batch.return_value.commit = mock_commit

                await SyncService.sync_market_data()

                # Assertions
                # Should be called for each ticker
                assert mock_fetch.call_count == len(mock_tickers)
                
                # Should only save the one successful result
                assert mock_set.call_count == 1
                mock_commit.assert_called_once()

                # Check the actual data that was passed to the batch set
                saved_data = mock_set.call_args[0][1]
                assert saved_data['ticker'] == 'AAPL'
                assert saved_data['close'] == 154.5
                assert saved_data['sma200'] == 175.5
                assert saved_data['vwma200'] == 176.2
                assert saved_data['rsi14'] == 65.75
                assert saved_data['atr14'] == 12.34
                assert 'sma7' in saved_data # Check a few other fields exist
                assert 'vwma50' in saved_data
