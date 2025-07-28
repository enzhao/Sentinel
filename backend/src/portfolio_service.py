from firebase_admin import firestore
from typing import List, Optional
from .models import PortfolioDB, CreatePortfolioRequest, UpdatePortfolioRequest, AddHoldingRequest, HoldingDB
from .firebase_setup import db

portfolios_collection = db.collection('portfolios')


# #############################################################################
# PORTFOLIO SERVICE
# #############################################################################

class PortfolioService:
    """
    A service class to handle all Firestore interactions for portfolios.
    """

    @staticmethod
    def create_portfolio(user_id: str, portfolio_data: CreatePortfolioRequest) -> Optional[PortfolioDB]:
        """
        Creates a new portfolio document in Firestore for a given user.
        Returns None if a portfolio with the same name already exists for the user.
        """
        # Rule P_E_1103: Check for unique portfolio name for the user
        existing_portfolios = PortfolioService.get_portfolios_by_user(user_id)
        if any(p.name == portfolio_data.name for p in existing_portfolios):
            return None

        new_portfolio = PortfolioDB(userId=user_id, **portfolio_data.model_dump())
        portfolios_collection.document(new_portfolio.portfolioId).set(new_portfolio.model_dump())
        return new_portfolio

    @staticmethod
    def get_portfolios_by_user(user_id: str) -> List[PortfolioDB]:
        """
        Retrieves a list of all portfolios for a given user.
        """
        docs = portfolios_collection.where('userId', '==', user_id).stream()
        return [PortfolioDB(**doc.to_dict()) for doc in docs]

    @staticmethod
    def get_portfolio_by_id(portfolio_id: str, user_id: str) -> Optional[PortfolioDB]:
        """
        Retrieves a single portfolio by its ID, ensuring it belongs to the user.
        """
        doc_ref = portfolios_collection.document(portfolio_id)
        doc = doc_ref.get()
        if not doc.exists:
            return None
        
        portfolio = PortfolioDB(**doc.to_dict())
        if portfolio.userId != user_id:
            # This is an authorization check. The user is trying to access a portfolio
            # that does not belong to them. We return None, and the API layer will
            # handle the HTTP 403/404 response.
            return None
            
        return portfolio

    @staticmethod
    def update_portfolio(portfolio_id: str, user_id: str, update_data: UpdatePortfolioRequest) -> Optional[PortfolioDB]:
        """
        Updates a portfolio's details.
        """
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        portfolios_collection.document(portfolio_id).update(update_dict)
        
        # Return the updated portfolio
        updated_portfolio_doc = portfolios_collection.document(portfolio_id).get()
        return PortfolioDB(**updated_portfolio_doc.to_dict())


    @staticmethod
    def delete_portfolio(portfolio_id: str, user_id: str) -> bool:
        """
        Deletes a portfolio, returning True if successful.
        """
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            return False
        
        portfolios_collection.document(portfolio_id).delete()
        return True

    @staticmethod
    def add_holding(portfolio_id: str, user_id: str, holding_data: AddHoldingRequest) -> Optional[PortfolioDB]:
        """
        Adds a new holding to a portfolio.
        """
        # Rule P_E_3104: Validate lot data
        for lot in holding_data.lots:
            if lot.quantity <= 0 or lot.purchasePrice <= 0:
                raise ValueError("Lot quantity and purchase price must be positive.")

        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            return None

        new_holding = HoldingDB(**holding_data.dict())
        
        # Use FieldValue to atomically add the new holding to the array
        portfolios_collection.document(portfolio_id).update({
            'holdings': firestore.ArrayUnion([new_holding.dict()])
        })

        updated_portfolio_doc = portfolios_collection.document(portfolio_id).get()
        return PortfolioDB(**updated_portfolio_doc.to_dict())

    @staticmethod
    def delete_holding(portfolio_id: str, user_id: str, holding_id: str) -> Optional[PortfolioDB]:
        """
        Deletes a holding from a portfolio.
        """
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            return None

        original_length = len(portfolio.holdings)
        portfolio.holdings = [h for h in portfolio.holdings if h.holdingId != holding_id]

        if len(portfolio.holdings) == original_length:
            # No holding was found/deleted
            return None

        portfolios_collection.document(portfolio_id).update({"holdings": [h.dict() for h in portfolio.holdings]})
        updated_portfolio_doc = portfolios_collection.document(portfolio_id).get()
        return PortfolioDB(**updated_portfolio_doc.to_dict())

    @staticmethod
    def delete_lot(portfolio_id: str, user_id: str, holding_id: str, lot_id: str) -> Optional[PortfolioDB]:
        """
        Deletes a lot from a holding within a portfolio.
        """
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            return None

        holding_found = False
        lot_deleted = False
        for holding in portfolio.holdings:
            if holding.holdingId == holding_id:
                holding_found = True
                original_lot_count = len(holding.lots)
                holding.lots = [lot for lot in holding.lots if lot.lotId != lot_id]
                if len(holding.lots) < original_lot_count:
                    lot_deleted = True
                break
        
        if not holding_found or not lot_deleted:
            return None

        portfolios_collection.document(portfolio_id).update({"holdings": [h.dict() for h in portfolio.holdings]})
        updated_portfolio_doc = portfolios_collection.document(portfolio_id).get()
        return PortfolioDB(**updated_portfolio_doc.to_dict())


# Instantiate the service for use in the API routers
portfolio_service = PortfolioService()