# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import secrets

class Settings(BaseSettings):
    APP_NAME: str = "Ubuntu Agent Manager"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    ADMIN_KEY: str = "your-admin-key-here"  # Change this in production
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "agent_manager"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()