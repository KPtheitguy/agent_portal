# app/core/security.py
from fastapi import HTTPException, Header
from typing import Optional
from ..config.settings import get_settings

settings = get_settings()

async def validate_admin_key(admin_key: str = Header(..., alias="X-Admin-Key")) -> str:
    """Validate admin API key"""
    if admin_key != settings.ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin key"
        )
    return admin_key

async def validate_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Validate agent API key"""
    # You would typically check this against your database
    # For now, we'll just ensure it's not empty
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    return api_key

def generate_registration_token() -> str:
    """Generate a new registration token"""
    return secrets.token_urlsafe(32)

def verify_registration_token(token: str) -> bool:
    """Verify if a registration token is valid"""
    # You would typically check this against your database
    # For testing, return True
    return True