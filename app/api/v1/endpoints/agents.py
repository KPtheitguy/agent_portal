# app/api/v1/endpoints/agents.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from ....core import security
from ....config.settings import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/register/token", response_model=schemas.TokenResponse)
async def get_registration_token(
    token_request: schemas.TokenRequest,
    db: Session = Depends(get_db),
    x_admin_key: str = Header(..., alias="X-Admin-Key")
):
    """Generate a registration token for an agent"""
    # Verify admin key from header
    if x_admin_key != settings.ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin key"
        )

    token = security.generate_registration_token()
    
    # Store token in database
    db_token = models.RegistrationToken(
        token=token,
        environment=token_request.environment,
        description=token_request.description,
        expires_at=datetime.utcnow() + timedelta(hours=token_request.expiry_hours or 24)
    )
    
    db.add(db_token)
    db.commit()
    
    return {
        "token": token,
        "expires_at": db_token.expires_at
    }