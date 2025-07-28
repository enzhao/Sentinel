from typing import Dict, List

# This is a mock data source. In the future, this will be replaced with a real
# implementation that calls the Alpha Vantage API.
MOCK_MARKET_DATA = {
    "VOO": {"price": 410.50},
    "AAPL": {"price": 175.20},
    "QQQ.DE": {"price": 380.75},
    "GOOGL": {"price": 135.00},
    # Add any other tickers you use for testing here
}

class MarketDataService:
    """
    A service to fetch market data.
    For now, it uses a mock data source.
    """

    @staticmethod
    def get_market_data_for_tickers(tickers: List[str]) -> Dict[str, Dict]:
        """
        Fetches the latest market data for a list of stock tickers.

        Args:
            tickers: A list of stock tickers (e.g., ["VOO", "AAPL"]).

        Returns:
            A dictionary where keys are tickers and values are their market data.
            Example: {"VOO": {"price": 410.50}, "AAPL": {"price": 175.20}}
        """
        print(f"Fetching mock market data for tickers: {tickers}")
        
        # In a real implementation, you would handle tickers not found in the API.
        # For this mock, we'll return a default price for any unknown ticker.
        return {
            ticker: MOCK_MARKET_DATA.get(ticker, {"price": 100.00})
            for ticker in tickers
        }

# Instantiate the service for use in other parts of the application
market_data_service = MarketDataService()
