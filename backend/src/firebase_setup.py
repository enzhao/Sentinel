import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK, ensuring it only runs once.
    This function is safe to call multiple times.
    """
    if not firebase_admin._apps:
        print("Initializing Firebase App...")
        if os.getenv('ENV') == 'local':
            # Use service account key file for local development
            key_path = 'serviceAccountKey.json'
            if not os.path.exists(key_path):
                 # Look in the parent directory if running from src
                key_path = os.path.join('..', key_path)

            if not os.path.exists(key_path):
                 raise FileNotFoundError(
                    "Running locally, but 'serviceAccountKey.json' not found in 'backend/' or 'backend/src/'. "
                    "Please follow the setup instructions in the README."
                )
            print(f"Found service account key at: {key_path}")
            cred = credentials.Certificate(key_path)
        else:
            # Use application default credentials for deployed environments (Cloud Run)
            print("Running in production mode. Initializing with ADC...")
            cred = credentials.ApplicationDefault()
        
        firebase_admin.initialize_app(cred)
        print("✅ Firebase App initialized.")
    else:
        print("Firebase App already initialized.")

# Run the initialization when this module is imported.
initialize_firebase_app()

# Firestore client
db = firestore.client()
