import os
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK, ensuring it only runs once.
    This function is safe to call multiple times.
    """
    if not firebase_admin._apps:
        print("Initializing Firebase App...")
        if os.getenv('ENV') == 'local':
            # Build an absolute path to the key file relative to this script's location
            key_path = Path(__file__).parent.parent / "serviceAccountKey.json"
            
            if not key_path.exists():
                 raise FileNotFoundError(
                    f"Running locally, but 'serviceAccountKey.json' not found at the expected path: {key_path}. "
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