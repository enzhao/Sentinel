import datetime
from typing import Optional, Dict, Any

class IdempotencyService:
    """
    Handles the storage and retrieval of idempotent responses in Firestore.
    """
    def __init__(self, db_client):
        self.db = db_client
        self.collection = self.db.collection('idempotencyKeys')

    def get_idempotent_response(self, idempotency_key: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a stored response if the idempotency key exists and belongs to the user.

        Returns:
            The stored response document or None if not found.
        """
        doc_ref = self.collection.document(idempotency_key)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        # Security check: ensure the key was created by the same user
        if data.get("userId") != user_id:
            # This is a security measure to prevent one user from replaying another's key
            return None 
        
        return data.get("response")

    def store_idempotent_response(self, idempotency_key: str, user_id: str, response_data: Dict[str, Any]):
        """
        Stores a new response against an idempotency key.
        """
        doc_ref = self.collection.document(idempotency_key)
        doc_data = {
            "userId": user_id,
            "createdAt": datetime.datetime.now(datetime.timezone.utc),
            "expireAt": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
            "response": response_data
        }
        doc_ref.set(doc_data)


