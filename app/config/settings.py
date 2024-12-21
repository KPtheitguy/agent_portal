# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Agent Manager"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    ADMIN_KEY: str
    SECRET_KEY: str

    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()