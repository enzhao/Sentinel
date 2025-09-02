import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

# --- Environment Loading ---
# This logic MUST run before any other application modules are imported.
# It reads the ENV variable and loads the corresponding .env file.
ENV = os.environ.get("ENV", "dev")
env_path = Path(__file__).parent.parent / f".env.{ENV}"

if env_path.exists():
    print(f"DIAGNOSTIC: Loading environment from: {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    print(f"DIAGNOSTIC: No .env file found for ENV='{ENV}'. Using system environment variables.")
# --- End Environment Loading ---

# --- Module Imports (after environment is loaded) ---
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .firebase_setup import initialize_firebase_app
from .middleware import idempotency_middleware
from .routers.user_router import router as user_router
from .routers.portfolio_router import router as portfolio_router
# --- End Module Imports ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    This is the recommended place for initialization logic.
    """
    print("DIAGNOSTIC: Application startup...")
    # Initialize Firebase Admin SDK on startup.
    # This ensures all configurations and connections are ready.
    initialize_firebase_app()
    yield
    # Shutdown logic can be placed here if needed.
    print("DIAGNOSTIC: Application shutdown.")

app = FastAPI(
    title="Sentinel API",
    description="Backend API for the Sentinel investment monitoring tool.",
    lifespan=lifespan,
)

# --- CORS Middleware Configuration ---
# The order of middleware is important. They are processed in the order they are added.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://sentinel-invest.web.app",
    "https://sentinel-invest.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# The idempotency middleware should run after CORS but before the request hits the router.
app.middleware("http")(idempotency_middleware)
# --- End of CORS Configuration ---

# --- API Routers ---
# Include the main user router. As more features are added,
# their routers will be included here as well.
app.include_router(user_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")
# --- End of API Routers ---

@app.get("/")
def read_root():
    """A simple health-check endpoint."""
    return {"message": "Welcome to the Sentinel Backend API!"}
