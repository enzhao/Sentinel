from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4

from ..core.internal_models import PortfolioDB
from ..api.models import PortfolioCreationRequest, PortfolioSummary, Currency, CashReserve
from ..core.utils import convert_uuids_to_str

class PortfolioService:
    def __init__(self, db_client):
        self.db = db_client
        self.portfolios_collection = self.db.collection("portfolios")

    def create_portfolio(self, user_id: str, portfolio_data: dict) -> PortfolioDB:
        """
        Creates a new portfolio in Firestore.
        Reference: product_spec.md#331-p_1000-portfolio-creation
        """
        now = datetime.now(timezone.utc)
        new_portfolio_id = uuid4()

        portfolio_data["portfolioId"] = new_portfolio_id
        portfolio_data["userId"] = user_id
        portfolio_data["ruleSetId"] = None  # New portfolios start without a rule set
        portfolio_data["createdAt"] = now
        portfolio_data["modifiedAt"] = now

        firestore_safe_data = convert_uuids_to_str(portfolio_data)
        self.portfolios_collection.document(str(new_portfolio_id)).set(firestore_safe_data)
        return PortfolioDB(**firestore_safe_data)

    def get_portfolio_by_id(self, portfolio_id: UUID4) -> Optional[PortfolioDB]:
        """
        Retrieves a single portfolio by its ID.
        Reference: product_spec.md#3321-p_2000-single-portfolio-retrieval
        """
        portfolio_doc = self.portfolios_collection.document(str(portfolio_id)).get()
        if portfolio_doc.exists:
            return PortfolioDB(**portfolio_doc.to_dict())
        return None

    def get_portfolios_by_user(self, user_id: str) -> List[PortfolioDB]:
        """
        Retrieves all portfolios for a given user.
        Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval
        """
        # For now, return full Portfolio objects. Later, this might return PortfolioSummary.
        portfolio_docs = self.portfolios_collection.where("userId", "==", user_id).stream()
        portfolios = [PortfolioDB(**doc.to_dict()) for doc in portfolio_docs]
        return portfolios
    
    