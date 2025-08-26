from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.dependencies import get_current_user
from src.routers.user_router import router as user_router
from src.firebase_setup import db
from src.middleware import idempotency_middleware
import src.messages  # Initialize the message manager

app = FastAPI()

# The idempotency middleware should be one of the first to run.
app.middleware("http")(idempotency_middleware)

app.include_router(user_router, prefix="/api/v1")

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



