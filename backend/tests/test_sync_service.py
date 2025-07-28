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
    Tests the main sync logic, ensuring OHLC and all indicators are fetched and saved.
    """
    mock_tickers = {"AAPL"}
    
    # Mock the responses from all Alpha Vantage service calls
    mock_aapl_data = MarketDataDB(ticker="AAPL", open=1, high=2, low=3, close=200.5, volume=100)
    mock_aapl_ma200 = 175.0
    mock_aapl_rsi = 65.0
    mock_aapl_atr = 10.5
    
    with patch('src.services.sync_service.SyncService.get_all_unique_tickers', new_callable=AsyncMock, return_value=mock_tickers):
        with patch('src.services.market_data_service.alpha_vantage_service.get_daily_data', new_callable=AsyncMock, return_value=mock_aapl_data) as mock_fetch_daily, \
             patch('src.services.market_data_service.alpha_vantage_service.get_ma200', new_callable=AsyncMock, return_value=mock_aapl_ma200) as mock_fetch_ma200, \
             patch('src.services.market_data_service.alpha_vantage_service.get_weekly_rsi', new_callable=AsyncMock, return_value=mock_aapl_rsi) as mock_fetch_rsi, \
             patch('src.services.market_data_service.alpha_vantage_service.get_atr', new_callable=AsyncMock, return_value=mock_aapl_atr) as mock_fetch_atr:
            
            with patch('src.firebase_setup.db.batch') as mock_batch:
                mock_set = MagicMock()
                mock_batch.return_value.set = mock_set
                mock_commit = MagicMock()
                mock_batch.return_value.commit = mock_commit

                await SyncService.sync_market_data()

                # Assertions
                mock_fetch_daily.assert_awaited_once_with("AAPL")
                mock_fetch_ma200.assert_awaited_once_with("AAPL")
                mock_fetch_rsi.assert_awaited_once_with("AAPL")
                mock_fetch_atr.assert_awaited_once_with("AAPL")
                
                assert mock_set.call_count == 1
                mock_commit.assert_called_once()

                # Check the actual data that was passed to the batch set
                saved_data = mock_set.call_args[0][1]
                assert saved_data['ticker'] == 'AAPL'
                assert saved_data['close'] == 200.5
                assert saved_data['ma200'] == 175.0
                assert saved_data['rsi_weekly'] == 65.0
                assert saved_data['atr'] == 10.5
