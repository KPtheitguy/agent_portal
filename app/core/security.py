# app/core/security.py
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..config.settings import get_settings

settings = get_settings()

def verify_admin_key(admin_key: str) -> bool:
    """Verify if admin key is valid"""
    return admin_key == settings.ADMIN_KEY

def generate_registration_token() -> str:
    """Generate a new registration token"""
    return secrets.token_urlsafe(32)

def generate_api_key() -> str:
    """Generate a new API key"""
    return secrets.token_urlsafe(48)

def verify_agent_api_key(db: Session, agent_id: str, api_key: str) -> bool:
    """Verify if agent API key is valid"""
    db_api_key = db.query(models.AgentApiKey).filter(
        models.AgentApiKey.agent_id == agent_id,
        models.AgentApiKey.key == api_key,
        models.AgentApiKey.revoked == False
    ).first()
    return db_api_key is not None