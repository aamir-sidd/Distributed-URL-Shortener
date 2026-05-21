from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Distributed URL Shortener"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Pydantic settings config to load variables from .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instantiate a global settings singleton
settings = Settings()
