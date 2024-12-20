# app/api/v1/endpoints/agents.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, Dict
from datetime import datetime
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from ....core import security

router = APIRouter()

@router.post("/register/token")
async def get_registration_token(
    request: schemas.TokenRequest,
    db: Session = Depends(get_db)
):
    """Get a registration token for an agent"""
    if not security.verify_admin_key(request.admin_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid admin key"
        )
    
    token = security.generate_registration_token()
    
    # Store token in database
    db_token = models.RegistrationToken(
        token=token,
        environment=request.environment,
        description=request.description,
        expires_at=datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    )
    db.add(db_token)
    db.commit()
    
    return {
        "token": token,
        "expires_at": db_token.expires_at
    }

@router.post("/register/agent", response_model=schemas.Agent)
async def register_agent(
    agent: schemas.AgentRegister,
    db: Session = Depends(get_db)
):
    """Register a new agent with a token"""
    # Verify token
    db_token = db.query(models.RegistrationToken).filter(
        models.RegistrationToken.token == agent.registration_token,
        models.RegistrationToken.used == False,
        models.RegistrationToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired registration token"
        )
    
    try:
        # Create new agent
        new_agent = models.Agent(
            hostname=agent.hostname,
            ip_address=agent.ip_address,
            environment=db_token.environment,
            description=agent.description or db_token.description,
            version=agent.version,
            os_info=agent.os_info,
            status='active',
            last_seen=datetime.utcnow()
        )
        
        db.add(new_agent)
        
        # Mark token as used
        db_token.used = True
        db_token.used_by = new_agent.id
        db_token.used_at = datetime.utcnow()
        
        db.commit()
        db.refresh(new_agent)
        
        # Generate API key for future communications
        api_key = security.generate_api_key()
        db_api_key = models.AgentApiKey(
            agent_id=new_agent.id,
            key=api_key,
            created_at=datetime.utcnow()
        )
        
        db.add(db_api_key)
        db.commit()
        
        return {
            "agent": new_agent,
            "api_key": api_key
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/{agent_id}")
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    api_key: str = Header(..., alias="X-API-Key")
):
    """Get agent details"""
    if not security.verify_agent_api_key(db, agent_id, api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent