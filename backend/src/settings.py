import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Determine the environment, default to 'local'
APP_ENV = os.getenv("APP_ENV", "local")

# --- This is the key change ---
# Build the path to the .env file relative to this settings.py file.
# This makes the path independent of where the script is run from.
env_file_path = Path(__file__).parent.parent / ".env"
if APP_ENV == "test":
    env_file_path = Path(__file__).parent.parent / ".env.test"
# -----------------------------

class Settings(BaseSettings):
    """
    Manages application settings and secrets.
    Reads from the appropriate .env file based on APP_ENV.
    """
    APP_ENV: str = APP_ENV
    ALPHA_VANTAGE_API_KEY: str

    # This tells Pydantic which .env file to load
    model_config = SettingsConfigDict(env_file=env_file_path, extra='ignore')

# Create a single, reusable instance of the settings
settings = Settings()

print(f"✅ Settings loaded for APP_ENV: {settings.APP_ENV} from {env_file_path}")