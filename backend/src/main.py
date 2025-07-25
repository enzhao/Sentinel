import os
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Firebase Initialization ---
# Initialize with ADC by default (works on Cloud Run)
try:
    firebase_admin.initialize_app()
    db = firestore.client()
    print("Successfully connected to Firestore using ADC.")
except Exception as e:
    print(f"Error connecting to Firestore: {e}")
    db = None

# For local development, use service account key if ENV is set
if os.getenv("ENV") == "local":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_KEY_PATH = os.path.join(BASE_DIR, '..', 'serviceAccountKey.json')
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        # Re-initialize with service account key for local
        firebase_admin.initialize_app(cred, name="local")
        db = firestore.client()
        print("Successfully connected to Firestore using service account key.")
    except Exception as e:
        print(f"Error connecting to Firestore locally: {e}")
        db = None
# --- End of Firebase Initialization ---

app = FastAPI()

# --- CORS Middleware Configuration ---
origins = [
    "http://localhost:5173",  # Vue dev server
    "https://sentinel-invest.web.app",  # Production frontend
    "https://sentinel-invest.firebaseapp.com",  # Firebase hosting
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- End of CORS Configuration ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentinel Backend API!"}

@app.get("/api/message")
def get_dummy_message():
    if not db:
        raise HTTPException(status_code=500, detail="Firestore client not initialized.")
    try:
        doc_ref = db.collection('settings').document('dummyMessage')
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dummy message document not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    