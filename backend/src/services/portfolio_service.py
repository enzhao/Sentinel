from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4

from ..api.models import Portfolio, PortfolioCreationRequest, PortfolioSummary, Currency, CashReserve
from ..firebase_setup import db
from ..core.utils import convert_uuids_to_str

portfolios_collection = db.collection("portfolios")

class PortfolioService:
    def create_portfolio(self, user_id: str, portfolio_data: PortfolioCreationRequest) -> Portfolio:
        """
        Creates a new portfolio in Firestore.
        Reference: product_spec.md#331-p_1000-portfolio-creation
        """
        now = datetime.now(timezone.utc)
        new_portfolio_id = uuid4()

        new_portfolio = Portfolio(
            portfolioId=new_portfolio_id,
            userId=user_id,
            name=portfolio_data.name,
            description=portfolio_data.description,
            defaultCurrency=portfolio_data.defaultCurrency,
            cashReserve=portfolio_data.cashReserve,
            ruleSetId=None, # New portfolios start without a rule set
            createdAt=now,
            modifiedAt=now
        )
        portfolios_collection.document(str(new_portfolio_id)).set(convert_uuids_to_str(new_portfolio.model_dump()))
        return new_portfolio

    def get_portfolio_by_id(self, portfolio_id: UUID4) -> Optional[Portfolio]:
        """
        Retrieves a single portfolio by its ID.
        Reference: product_spec.md#3321-p_2000-single-portfolio-retrieval
        """
        portfolio_doc = portfolios_collection.document(str(portfolio_id)).get()
        if portfolio_doc.exists:
            return Portfolio(**portfolio_doc.to_dict())
        return None

    def get_portfolios_by_user(self, user_id: str) -> List[Portfolio]:
        """
        Retrieves all portfolios for a given user.
        Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval
        """
        # For now, return full Portfolio objects. Later, this might return PortfolioSummary.
        portfolio_docs = portfolios_collection.where("userId", "==", user_id).stream()
        portfolios = [Portfolio(**doc.to_dict()) for doc in portfolio_docs]
        return portfolios

portfolio_service = PortfolioService()