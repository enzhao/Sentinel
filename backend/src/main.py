from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth import get_current_user
from .routers import user_router
from .firebase_setup import db
from .middleware import idempotency_middleware

app = FastAPI()

# The idempotency middleware should be one of the first to run.
app.middleware("http")(idempotency_middleware)

app.include_router(user_router.router, prefix="/api")

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
