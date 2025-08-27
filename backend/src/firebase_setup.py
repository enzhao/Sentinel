import os
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK, ensuring it only runs once.
    Connects to emulators if ENV=test, otherwise uses cloud credentials.
    """
    if not firebase_admin._apps:
        print("Initializing Firebase App...")

        # 1. Development and Test Environment, be it local or cloud (use Eumlators for pytest, CI/CD)
        if os.getenv('ENV') == 'dev':
            print("Running in TEST mode. Connecting to Firebase Emulators...")
            # These environment variables are special names the Admin SDK looks for.
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
            os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"
            
            # When using emulators, you don't need real credentials.
            # A dummy project ID is sufficient.
            firebase_admin.initialize_app(options={
                'projectId': 'sentinel-test',
            })

        # 2. Local Production Environment (app on local machine -> real database)
        elif os.getenv('ENV') == 'local-prod':
            key_path = Path(__file__).parent.parent / "serviceAccountKey.json"
            if not key_path.exists():
                 raise FileNotFoundError(
                    f"Running locally, but 'serviceAccountKey.json' not found at the expected path: {key_path}. "
                    "Please follow the setup instructions in the README."
                )
            print(f"Found service account key at: {key_path}")
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)

        # 3. Deployed Production Environment (Cloud Run, etc.)
        else:
            print("Running in production/deployed mode. Initializing with ADC...")
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        
        print("✅ Firebase App initialized.")
    else:
        print("Firebase App already initialized.")

# Run the initialization when this module is imported.
initialize_firebase_app()

# Firestore client
db = firestore.client()

