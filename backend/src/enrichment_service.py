from typing import Dict
from .models import Portfolio, Holding, Lot
from .firebase_setup import db
from datetime import datetime

class EnrichmentService:
    """
    A service to enrich portfolio data with computed values using market
    data stored in our local Firestore database.
    """

    @staticmethod
    def get_latest_prices_from_db(tickers: list[str]) -> Dict[str, float]:
        """
        Fetches the most recent closing price for each ticker from the
        /marketData collection in Firestore.
        """
        prices = {}
        today_str = datetime.now().strftime('%Y-%m-%d')

        for ticker in tickers:
            # Path to today's market data document for the ticker
            doc_ref = db.collection('marketData').document(ticker).collection('dailyPrices').document(today_str)
            doc = doc_ref.get()
            
            if doc.exists:
                prices[ticker] = doc.to_dict().get('close', 0.0)
            else:
                # Fallback: If today's data isn't synced yet, you might want to
                # get the most recent document. For simplicity, we'll default to 0.
                # A more robust implementation would query the last document ordered by date.
                print(f"Warning: No market data found for {ticker} for date {today_str}. Defaulting price to 0.")
                prices[ticker] = 0.0
        
        return prices

    @staticmethod
    def enrich_portfolio(portfolio_db: Portfolio) -> Portfolio:
        """
        Enriches a portfolio object with calculated data like current value and profit/loss.
        """
        tickers = {holding.ticker for holding in portfolio_db.holdings}
        if not tickers:
            return Portfolio(**portfolio_db.model_dump())

        # 1. Fetch the latest prices from our own database
        latest_prices = EnrichmentService.get_latest_prices_from_db(list(tickers))

        # 2. Enrich each holding and lot
        total_portfolio_cost = 0.0
        total_portfolio_value = 0.0

        enriched_holdings = []
        for holding_db in portfolio_db.holdings:
            current_price = latest_prices.get(holding_db.ticker, 0.0)
            
            total_holding_cost = 0.0
            total_holding_value = 0.0
            
            enriched_lots = []
            for lot_db in holding_db.lots:
                lot_cost = lot_db.quantity * lot_db.purchasePrice
                lot_value = lot_db.quantity * current_price
                pre_tax_profit = lot_value - lot_cost
                
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

            pre_tax_gain_loss_holding = total_holding_value - total_holding_cost
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

        # 3. Enrich the final Portfolio object
        pre_tax_gain_loss_portfolio = total_portfolio_value - total_portfolio_cost
        after_tax_gain_loss_portfolio = pre_tax_gain_loss_portfolio * (1 - portfolio_db.taxSettings.capitalGainTaxRate / 100)
        gain_loss_percentage_portfolio = (pre_tax_gain_loss_portfolio / total_portfolio_cost) * 100 if total_portfolio_cost > 0 else 0

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
