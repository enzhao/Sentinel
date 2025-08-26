from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from ..firebase_setup import db
from ..api.models import User, Portfolio
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

class UserService:
    def create_user_document(self, uid: str, email: str, username: str, default_portfolio_id: UUID) -> User:
        user_data = {
            "uid": uid,
            "email": email,
            "username": username,
            "defaultPortfolioId": str(default_portfolio_id),
            "subscriptionStatus": "FREE",
            "notificationPreferences": {"email": True, "push": False},
            "createdAt": datetime.now(timezone.utc),
            "modifiedAt": datetime.now(timezone.utc),
        }
        db.collection("users").document(uid).set(user_data)
        return User(**user_data)

    def get_user_by_uid(self, uid: str) -> Optional[User]:
        user_doc = db.collection("users").document(uid).get()
        if user_doc.exists:
            return User(**user_doc.to_dict())
        return None

    def update_user_default_portfolio(self, uid: str, default_portfolio_id: UUID):
        user_doc_ref = db.collection("users").document(uid)
        user_doc_ref.update({
            "defaultPortfolioId": str(default_portfolio_id),
            "modifiedAt": datetime.now(timezone.utc)
        })

user_service = UserService()
