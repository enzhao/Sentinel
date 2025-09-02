from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4

from pydantic import UUID4
from google.cloud.firestore_v1.base_query import FieldFilter

from ..core.internal_models import PortfolioDB
if TYPE_CHECKING:
    from .user_service import UserService
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

    def get_portfolio_by_name(self, user_id: str, name: str) -> Optional[PortfolioDB]:
        """
        Retrieves a portfolio by its name for a specific user.
        Reference: product_spec.md#3.3.1-P_E_1103
        """
        query = self.portfolios_collection.where(
            filter=FieldFilter("userId", "==", user_id)
        ).where(
            filter=FieldFilter("name", "==", name)
        ).limit(1)
        docs = query.stream()
        for doc in docs:
            return PortfolioDB(**doc.to_dict())
        return None

    def get_portfolios_by_user(self, user_id: str) -> List[PortfolioDB]:
        """
        Retrieves all portfolios for a given user.
        Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval
        """
        query = self.portfolios_collection.where(filter=FieldFilter("userId", "==", user_id))
        portfolio_docs = query.stream()
        portfolios = [PortfolioDB(**doc.to_dict()) for doc in portfolio_docs]
        return portfolios

    def update_portfolio(self, portfolio_id: UUID4, update_data: dict) -> Optional[PortfolioDB]:
        """
        Updates a portfolio document in Firestore.
        Reference: product_spec.md#3.3.3.1-P_3000-Portfolio-Update-(Manual)
        """
        portfolio_ref = self.portfolios_collection.document(str(portfolio_id))

        # Add modifiedAt timestamp
        update_data["modifiedAt"] = datetime.now(timezone.utc)

        firestore_safe_data = convert_uuids_to_str(update_data)
        portfolio_ref.update(firestore_safe_data)

        updated_doc = portfolio_ref.get()
        if updated_doc.exists:
            return PortfolioDB(**updated_doc.to_dict())
        return None

    def delete_portfolio(self, user_id: str, portfolio_id: UUID4, user_service: 'UserService'):
        """
        Deletes a portfolio document from Firestore and handles default portfolio reassignment.
        Reference: product_spec.md#3.3.4.1-P_4000-Portfolio-Deletion-(Entire-Portfolio)
        """
        user = user_service.get_user_by_uid(user_id)
        if user and user.defaultPortfolioId == portfolio_id:
            # The portfolio being deleted is the default one. We need to reassign.
            other_portfolios = [p for p in self.get_portfolios_by_user(user_id) if p.portfolioId != portfolio_id]
            
            new_default_id = None
            if other_portfolios:
                # P_I_4003: Auto-set new default if other portfolios exist.
                # We'll just pick the first one. The frontend can offer a choice later if desired.
                new_default_id = other_portfolios[0].portfolioId
            
            # Update the user's defaultPortfolioId
            user_service.update_user_settings(user_id, {"defaultPortfolioId": new_default_id})

        # For now, this just deletes the portfolio document.
        # In the future, it will also need to delete associated holdings, rules, etc. in a transaction.
        self.portfolios_collection.document(str(portfolio_id)).delete()