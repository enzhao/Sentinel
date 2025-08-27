from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from ..core.internal_models import UserDB, NotificationChannel
from ..api.models import PortfolioCreationRequest, Currency, CashReserve
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID
from .portfolio_service import PortfolioService

from ..core.utils import convert_uuids_to_str
from ..core.model_mappers import portfolio_creation_request_to_dict

class UserService:
    def __init__(self, db_client, portfolio_service_instance: PortfolioService):
        self.db = db_client
        self.portfolio_service = portfolio_service_instance

    def create_user_document(self, uid: str, email: str, username: str, default_portfolio_id: UUID) -> UserDB:
        user_data = {
            "uid": uid,
            "email": email,
            "username": username,
            "defaultPortfolioId": str(default_portfolio_id),
            "subscriptionStatus": "FREE",
            "notificationPreferences": [NotificationChannel.EMAIL.value],
            "createdAt": datetime.now(timezone.utc),
            "modifiedAt": datetime.now(timezone.utc),
        }
        self.db.collection("users").document(uid).set(user_data)
        return UserDB(**user_data)

    def get_user_by_uid(self, uid: str) -> Optional[UserDB]:
        user_doc = self.db.collection("users").document(uid).get()
        if user_doc.exists:
            return UserDB(**user_doc.to_dict())
        return None

    def update_user_default_portfolio(self, uid: str, default_portfolio_id: UUID):
        user_doc_ref = self.db.collection("users").document(uid)
        user_doc_ref.update({
            "defaultPortfolioId": str(default_portfolio_id),
            "modifiedAt": datetime.now(timezone.utc)
        })

    def update_user_settings(self, uid: str, update_data: dict) -> UserDB:
        user_doc_ref = self.db.collection("users").document(uid)

        # Validate defaultPortfolioId if present in update_data
        if "defaultPortfolioId" in update_data and update_data["defaultPortfolioId"] is not None:
            portfolio_id = update_data["defaultPortfolioId"]
            portfolio_doc_ref = self.db.collection("portfolios").document(str(portfolio_id))
            portfolio_doc = portfolio_doc_ref.get()
            if not portfolio_doc.exists or portfolio_doc.to_dict().get("userId") != uid:
                raise ValueError("US_E_3102: Invalid default portfolio specified.")

        # Explicitly convert Enum members to their string values before saving.
        if "notificationPreferences" in update_data:
            preferences = update_data["notificationPreferences"]
            if not isinstance(preferences, list):
                raise ValueError("notificationPreferences must be a list")
            valid_channels = {channel.value for channel in NotificationChannel}
            update_data["notificationPreferences"] = [
                pref.value if isinstance(pref, NotificationChannel) else pref
                for pref in preferences
            ]
            if not all(pref in valid_channels for pref in update_data["notificationPreferences"]):
                raise ValueError("Invalid notification preference values")
        
        update_data["modifiedAt"] = datetime.now(timezone.utc)
        
        # Convert any UUIDs in the update_data to strings before saving
        firestore_safe_data = convert_uuids_to_str(update_data)
        
        user_doc_ref.update(firestore_safe_data)
        
        updated_user_doc = user_doc_ref.get()
        return UserDB(**updated_user_doc.to_dict())

# Reference: product_spec.md#831-u_1000-user-provisioning-backend-script
# Reference: product_spec.md#931-us_1000-user-settings-creation
def create_firebase_user_and_user_document(email: str, password: str, username: str, db_client, portfolio_service_instance: PortfolioService):
    try:
        # Create user in Firebase Authentication
        firebase_user = auth.create_user(email=email, password=password, display_name=username)
        uid = firebase_user.uid

        # Create a default portfolio for the user
        # This is a minimal portfolio creation, actual logic might be in portfolio_service
        default_portfolio_data = PortfolioCreationRequest(
            name="My First Portfolio",
            description="Your default portfolio.",
            defaultCurrency=Currency.EUR,
            cashReserve=CashReserve(totalAmount=0.0, warChestAmount=0.0)
        )
        
        portfolio_dict = portfolio_creation_request_to_dict(default_portfolio_data)
        new_portfolio = portfolio_service_instance.create_portfolio(user_id=uid, portfolio_data=portfolio_dict)
        default_portfolio_id = new_portfolio.portfolioId

        # Create user document in Firestore
        user_service_instance = UserService(db_client, portfolio_service_instance)
        user_service_instance.create_user_document(uid, email, username, default_portfolio_id)
        
        print(f"Successfully created new user: {uid} and default portfolio: {default_portfolio_id}")
        return uid
    except FirebaseError as e:
        print(f"Error creating user: {e}")
        raise
    