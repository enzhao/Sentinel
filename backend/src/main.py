import os
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException

# --- Firebase Initialization ---
# Get the absolute path to the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the service account key
SERVICE_ACCOUNT_KEY_PATH = os.path.join(BASE_DIR, '..', 'serviceAccountKey.json')

# Initialize the Firebase Admin SDK
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Successfully connected to Firestore.")
except Exception as e:
    print(f"Error connecting to Firestore: {e}")
    db = None
# --- End of Firebase Initialization ---


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentinel Backend API!"}

@app.get("/api/message")
def get_dummy_message():
    if not db:
        raise HTTPException(status_code=500, detail="Firestore client not initialized.")
    try:
        # Reference the document we are going to create
        doc_ref = db.collection('settings').document('dummyMessage')
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dummy message document not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    