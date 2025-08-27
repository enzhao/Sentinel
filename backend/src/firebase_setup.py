import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

from google.auth import credentials as auth_credentials

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK. It's designed to run once.
    
    This function intelligently selects the authentication method based on
    the environment.
    """
    if not firebase_admin._apps:
        print("Initializing Firebase App...")
        
        cred = None
        options = {}

        # Priority 1: Check for Emulator environment
        if "FIRESTORE_EMULATOR_HOST" in os.environ:
            print("DIAGNOSTIC: Emulator detected. Using AnonymousCredentials.")
            cred = auth_credentials.AnonymousCredentials()
            options = {"projectId": os.environ.get("GCLOUD_PROJECT", "sentinel-invest")}

        # Priority 2: Check for an explicit service account key path via environment variable
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            print(f"DIAGNOSTIC: Found GOOGLE_APPLICATION_CREDENTIALS. Using key file: {key_path}")
            cred = credentials.Certificate(key_path)
        
        # Priority 3: Automatically find the service account key in the default location
        else:
            # Construct the path to the key file relative to this script's location
            # (src/firebase_setup.py -> backend/serviceAccountKey.json)
            key_path = Path(__file__).parent.parent / "serviceAccountKey.json"
            if key_path.exists():
                print(f"DIAGNOSTIC: Found key file at default location: {key_path}")
                cred = credentials.Certificate(key_path)
            
            # Priority 4: Fallback to Application Default Credentials
            # This is used when running in GCP or when authenticated with `gcloud auth`.
            else:
                print("DIAGNOSTIC: No emulator or key file found. Using ApplicationDefault credentials.")
                cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(cred, options)
        
        print("✅ Firebase App initialized.")

def get_db_client():
    """
    Returns a Firestore client.
    Ensures Firebase is initialized before returning the client.
    """
    if not firebase_admin._apps:
        initialize_firebase_app()
    return firestore.client()
