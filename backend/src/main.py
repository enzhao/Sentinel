import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

# --- Environment Loading ---
# This logic MUST run before any other application modules are imported.
# It reads the ENV variable and loads the corresponding .env file.
print("DIAGNOSTIC: Checking for environment configuration...")
env = os.environ.get("ENV", "dev")  # Default to 'dev' if not set
env_path = Path(__file__).parent.parent / f".env.{env}"

if env_path.exists():
    print(f"DIAGNOSTIC: Loading environment from: {env_path}")

    # Get variables from .env file to print them for diagnostics
    loaded_vars = dotenv_values(dotenv_path=env_path)
    if loaded_vars:
        print("DIAGNOSTIC: The following variables were found in the .env file:")
        for key, value in loaded_vars.items():
            print(f"  - {key} = '{value}'")

    # Now, actually load them into the environment
    load_dotenv(dotenv_path=env_path)
else:
    print(f"DIAGNOSTIC: No .env file found for ENV='{env}'. Using system environment variables.")
# --- End Environment Loading ---

# --- Diagnostic Check for Emulator ---
# This check runs after loading to confirm the final state of the environment.
print("DIAGNOSTIC: Verifying key environment variables...")
if os.environ.get("FIRESTORE_EMULATOR_HOST"):
    print(f"  ✅ FIRESTORE_EMULATOR_HOST is set to: {os.environ['FIRESTORE_EMULATOR_HOST']}")
else:
    print("  ❌ FIRESTORE_EMULATOR_HOST is NOT set. Backend will target LIVE Firestore.")

if os.environ.get("FIREBASE_AUTH_EMULATOR_HOST"):
    print(f"  ✅ FIREBASE_AUTH_EMULATOR_HOST is set to: {os.environ['FIREBASE_AUTH_EMULATOR_HOST']}")
else:
    print("  ❌ FIREBASE_AUTH_EMULATOR_HOST is NOT set. Backend will target LIVE Auth.")
# --- End Diagnostic Check ---

# --- Firebase Initialization ---
# This MUST be done after loading the environment and before importing any
# modules (like routers or middleware) that depend on a configured Firebase app.
from .firebase_setup import initialize_firebase_app
initialize_firebase_app()
# --- End Firebase Initialization ---


from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .middleware import idempotency_middleware
# from .messages import message_manager

# Import the router directly, not the factory function
from .routers.user_router import router as user_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    - Initializes the Firebase app.
    - Loads user-facing messages.
    """
    print("DIAGNOSTIC: Application startup event triggered.")
    # message_manager.load_messages() # This can remain here if needed

# The idempotency middleware should be one of the first to run.
app.middleware("http")(idempotency_middleware)

# Include the router directly. FastAPI will handle the dependencies at the endpoint level.
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

# This endpoint is just for demonstration and can be removed if not needed.
from src.dependencies import get_db

@app.get("/api/message")
def get_dummy_message(db=Depends(get_db)):
    try:
        doc_ref = db.collection('settings').document('dummyMessage')
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dummy message document not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
