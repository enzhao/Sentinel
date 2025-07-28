import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.models import PortfolioDB, HoldingDB, LotDB, TaxSettings
from src.enrichment_service import enrichment_service

@pytest.fixture
def sample_portfolio_db():
    """Provides a sample portfolio for testing."""
    return PortfolioDB(
        userId="test-user",
        name="Test Portfolio",
        holdings=[
            HoldingDB(
                ticker="AAPL",
                lots=[
                    LotDB(purchaseDate=datetime.now(), quantity=10, purchasePrice=150.0),
                    LotDB(purchaseDate=datetime.now(), quantity=5, purchasePrice=160.0),
                ]
            ),
            HoldingDB(
                ticker="GOOGL",
                lots=[
                    LotDB(purchaseDate=datetime.now(), quantity=2, purchasePrice=120.0)
                ]
            )
        ],
        taxSettings=TaxSettings(capitalGainTaxRate=25.0) # 25% for easy math
    )

def test_enrich_portfolio_calculations(sample_portfolio_db):
    """
    Tests the calculation logic of the enrichment service by mocking the DB call.
    """
    # Mock the database call within the enrichment service
    mock_prices = {
        "AAPL": 200.0,
        "GOOGL": 140.0,
    }

    with patch('src.enrichment_service.EnrichmentService.get_latest_prices_from_db', return_value=mock_prices):
        enriched_portfolio = enrichment_service.enrich_portfolio(sample_portfolio_db)

        # --- Assertions for AAPL Holding ---
        aapl_holding = next(h for h in enriched_portfolio.holdings if h.ticker == "AAPL")
        assert aapl_holding.totalCost == (10 * 150) + (5 * 160)  # 1500 + 800 = 2300
        assert aapl_holding.currentValue == 15 * 200  # 3000
        assert aapl_holding.preTaxGainLoss == 3000 - 2300  # 700
        assert aapl_holding.gainLossPercentage == (700 / 2300) * 100

        # --- Assertions for GOOGL Holding ---
        googl_holding = next(h for h in enriched_portfolio.holdings if h.ticker == "GOOGL")
        assert googl_holding.totalCost == 2 * 120  # 240
        assert googl_holding.currentValue == 2 * 140  # 280
        assert googl_holding.preTaxGainLoss == 280 - 240  # 40
        assert googl_holding.gainLossPercentage == (40 / 240) * 100

        # --- Assertions for Overall Portfolio ---
        assert enriched_portfolio.totalCost == 2300 + 240  # 2540
        assert enriched_portfolio.currentValue == 3000 + 280  # 3280
        assert enriched_portfolio.preTaxGainLoss == 700 + 40  # 740
        assert enriched_portfolio.afterTaxGainLoss == 740 * (1 - 0.25) # 555
        assert enriched_portfolio.gainLossPercentage == (740 / 2540) * 100
