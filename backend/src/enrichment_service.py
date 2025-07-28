from typing import Dict
from .models import Portfolio, Holding, Lot
from .market_data_service import MarketDataService

class EnrichmentService:
    """
    A service to enrich portfolio data with computed values.
    """

    @staticmethod
    def enrich_portfolio(portfolio_db: Portfolio) -> Portfolio:
        """
        Enriches a portfolio object with calculated data like current value and profit/loss.
        """
        # 1. Collect all unique tickers from the portfolio's holdings
        tickers = {holding.ticker for holding in portfolio_db.holdings}
        if not tickers:
            # If there are no holdings, no enrichment is needed
            return Portfolio(**portfolio_db.model_dump())

        # 2. Fetch market data for all tickers in one go
        market_data = MarketDataService.get_market_data_for_tickers(list(tickers))

        # 3. Enrich each holding and lot, and aggregate portfolio-level data
        total_portfolio_cost = 0.0
        total_portfolio_value = 0.0

        enriched_holdings = []
        for holding_db in portfolio_db.holdings:
            current_price = market_data.get(holding_db.ticker, {}).get("price", 0)
            
            total_holding_cost = 0.0
            total_holding_value = 0.0
            
            enriched_lots = []
            for lot_db in holding_db.lots:
                # Enrich Lot
                lot_cost = lot_db.quantity * lot_db.purchasePrice
                lot_value = lot_db.quantity * current_price
                pre_tax_profit = lot_value - lot_cost
                
                # Note: Tax calculation is simplified for this example
                capital_gain_tax = max(0, pre_tax_profit * (portfolio_db.taxSettings.capitalGainTaxRate / 100))
                after_tax_profit = pre_tax_profit - capital_gain_tax

                enriched_lot = Lot(
                    **lot_db.model_dump(),
                    currentPrice=current_price,
                    currentValue=lot_value,
                    preTaxProfit=pre_tax_profit,
                    capitalGainTax=capital_gain_tax,
                    afterTaxProfit=after_tax_profit
                )
                enriched_lots.append(enriched_lot)
                
                total_holding_cost += lot_cost
                total_holding_value += lot_value

            # Enrich Holding
            pre_tax_gain_loss_holding = total_holding_value - total_holding_cost
            # Note: After-tax gain/loss for a holding is complex; this is a simplification
            after_tax_gain_loss_holding = pre_tax_gain_loss_holding * (1 - portfolio_db.taxSettings.capitalGainTaxRate / 100)
            gain_loss_percentage_holding = (pre_tax_gain_loss_holding / total_holding_cost) * 100 if total_holding_cost > 0 else 0

            holding_data = holding_db.model_dump()
            holding_data['lots'] = enriched_lots

            enriched_holding = Holding(
                **holding_data,
                totalCost=total_holding_cost,
                currentValue=total_holding_value,
                preTaxGainLoss=pre_tax_gain_loss_holding,
                afterTaxGainLoss=after_tax_gain_loss_holding,
                gainLossPercentage=gain_loss_percentage_holding
            )
            enriched_holdings.append(enriched_holding)

            total_portfolio_cost += total_holding_cost
            total_portfolio_value += total_holding_value

        # Enrich Portfolio
        pre_tax_gain_loss_portfolio = total_portfolio_value - total_portfolio_cost
        after_tax_gain_loss_portfolio = pre_tax_gain_loss_portfolio * (1 - portfolio_db.taxSettings.capitalGainTaxRate / 100)
        gain_loss_percentage_portfolio = (pre_tax_gain_loss_portfolio / total_portfolio_cost) * 100 if total_portfolio_cost > 0 else 0

        # 4. Construct the final, fully enriched Portfolio object
        portfolio_data = portfolio_db.model_dump()
        portfolio_data['holdings'] = enriched_holdings

        enriched_portfolio = Portfolio(
            **portfolio_data,
            totalCost=total_portfolio_cost,
            currentValue=total_portfolio_value,
            preTaxGainLoss=pre_tax_gain_loss_portfolio,
            afterTaxGainLoss=after_tax_gain_loss_portfolio,
            gainLossPercentage=gain_loss_percentage_portfolio
        )
        
        return enriched_portfolio

# Instantiate the service
enrichment_service = EnrichmentService()
