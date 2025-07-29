from typing import Optional
from src.models import UserDB, UpdateUserSettingsRequest
from src.firebase_setup import db
from src.services.portfolio_service import portfolio_service # To validate portfolio ownership

users_collection = db.collection('users')

class UserService:
    @staticmethod
    def get_user(uid: str) -> Optional[UserDB]:
        """
        Retrieves a user document from Firestore.
        """
        doc = users_collection.document(uid).get()
        if doc.exists:
            return UserDB(**doc.to_dict())
        return None

    @staticmethod
    def create_user(uid: str, email: str, username: str) -> UserDB:
        """
        Creates a new user document in Firestore.
        """
        new_user = UserDB(uid=uid, email=email, username=username)
        users_collection.document(uid).set(new_user.model_dump())
        return new_user

    @staticmethod
    def update_user_settings(uid: str, settings: UpdateUserSettingsRequest) -> Optional[UserDB]:
        """
        Updates a user's settings.
        """
        # Ensure the user exists
        user = UserService.get_user(uid)
        if not user:
            return None

        # If changing default portfolio, validate that the user owns it
        if settings.defaultPortfolioId:
            portfolio = portfolio_service.get_portfolio_by_id(settings.defaultPortfolioId, uid)
            if not portfolio:
                # User does not own this portfolio or it doesn't exist
                raise ValueError("Invalid defaultPortfolioId")

        update_data = settings.model_dump(exclude_unset=True)
        users_collection.document(uid).update(update_data)

        return UserService.get_user(uid)

# Instantiate the service
user_service = UserService()
