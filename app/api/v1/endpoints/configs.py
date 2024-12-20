# app/api/v1/endpoints/configs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from datetime import datetime

router = APIRouter()

@router.post("/{agent_id}", response_model=schemas.NginxConfig)
def create_config(
    agent_id: str,
    config: schemas.NginxConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new nginx configuration for an agent"""
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_config = models.NginxConfig(**config.dict(), agent_id=agent_id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/{agent_id}", response_model=List[schemas.NginxConfig])
def get_configs(agent_id: str, db: Session = Depends(get_db)):
    """Get all nginx configurations for an agent"""
    configs = db.query(models.NginxConfig).filter(
        models.NginxConfig.agent_id == agent_id
    ).all()
    return configs

@router.put("/{config_id}", response_model=schemas.NginxConfig)
def update_config(
    config_id: str,
    config_update: schemas.NginxConfigCreate,
    db: Session = Depends(get_db)
):
    """Update nginx configuration"""
    db_config = db.query(models.NginxConfig).filter(
        models.NginxConfig.id == config_id
    ).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    for key, value in config_update.dict().items():
        setattr(db_config, key, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config

@router.delete("/{config_id}")
def delete_config(config_id: str, db: Session = Depends(get_db)):
    """Delete nginx configuration"""
    db_config = db.query(models.NginxConfig).filter(
        models.NginxConfig.id == config_id
    ).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    db.delete(db_config)
    db.commit()
    return {"status": "success", "message": "Configuration deleted"}