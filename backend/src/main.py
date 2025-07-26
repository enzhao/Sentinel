import os
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth import get_current_user

app = FastAPI()
db = None

# --- Firebase Initialization ---
if os.getenv("ENV") == "local":
    # For local development, use the service account key.
    print("Running in local mode. Initializing with service account key...")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_KEY_PATH = os.path.join(BASE_DIR, '..', 'serviceAccountKey.json')
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Successfully connected to Firestore using service account key.")
    except Exception as e:
        print(f"Error connecting to Firestore locally: {e}")
else:
    # For production on Cloud Run, use Application Default Credentials but be explicit.
    print("Running in production mode. Initializing with ADC...")
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")
        
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': project_id,
        })
        db = firestore.client()
        print(f"Successfully connected to Firestore for project {project_id} using ADC.")
    except Exception as e:
        print(f"Error connecting to Firestore with ADC: {e}")
# --- End of Firebase Initialization ---


# --- CORS Middleware Configuration ---
origins = [
    "http://localhost:5173",
    "https://sentinel-invest.web.app",
    "https://sentinel-invest.firebaseapp.com",
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

@app.get("/api/me")
def get_user_profile(user: dict = Depends(get_current_user)):
    return {"uid": user.get("uid"), "email": user.get("email")}
