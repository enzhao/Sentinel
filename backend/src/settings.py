import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine the environment, default to 'local'
APP_ENV = os.getenv("APP_ENV", "local")

# Determine the .env file to use
env_file = ".env.test" if APP_ENV == "test" else ".env"

class Settings(BaseSettings):
    """
    Manages application settings and secrets.
    Reads from the appropriate .env file based on APP_ENV.
    """
    APP_ENV: str = APP_ENV
    ALPHA_VANTAGE_API_KEY: str

    # This tells Pydantic which .env file to load
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

# Create a single, reusable instance of the settings
settings = Settings()

print(f"✅ Settings loaded for APP_ENV: {settings.APP_ENV} from {env_file}")
