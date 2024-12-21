# app/core/security.py
from fastapi import HTTPException, Header
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..config.settings import get_settings

settings = get_settings()

async def validate_admin_key(x_admin_key: str = Header(..., alias="X-Admin-Key")) -> str:
    """Validate admin API key from header"""
    if x_admin_key != settings.ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin key"
        )
    return x_admin_key

async def validate_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Validate agent API key from header"""
    # You would typically check this against your database
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    return x_api_key

def generate_registration_token() -> str:
    """Generate a new registration token"""
    return secrets.token_urlsafe(32)

def generate_api_key() -> str:
    """Generate a new API key"""
    return secrets.token_urlsafe(48)

def verify_admin_key(admin_key: str) -> bool:
    """Verify if admin key is valid"""
    return admin_key == settings.ADMIN_KEY

def verify_agent_api_key(db: Session, agent_id: str, api_key: str) -> bool:
    """Verify if agent API key is valid"""
    # Implement database check for API key
    return True  # Placeholder - implement actual verification