import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Use 'ENV' to be consistent with the rest of the project (e.g., conftest.py)
# Default to 'dev' for local development.
ENV = os.getenv("ENV", "dev")

# Build the path to the .env file relative to this settings.py file.
# This makes the path independent of where the script is run from.
env_file_path = Path(__file__).parent.parent / ".env"

# For tests, we might use a separate file with mock keys.
if ENV == "test":
    env_file_path = Path(__file__).parent.parent / ".env.test"
# For local-prod, we explicitly use the main .env file.
elif ENV == "local-prod":
    env_file_path = Path(__file__).parent.parent / ".env"
# In a real 'prod' environment, variables will be set in the cloud platform,
# but we can leave this for consistency.
elif ENV == "prod":
    env_file_path = None # Don't load any .env file in production

class Settings(BaseSettings):
    """
    Manages application settings and secrets.
    Reads from the appropriate .env file based on ENV.
    """
    ENV: str = ENV
    ALPHA_VANTAGE_API_KEY: str

    # This tells Pydantic which .env file to load
    # If env_file is None, it will only read from system environment variables.
    model_config = SettingsConfigDict(env_file=env_file_path, extra='ignore')

# Create a single, reusable instance of the settings
settings = Settings()

print(f"✅ Settings loaded for ENV: {settings.ENV} from {env_file_path}")
