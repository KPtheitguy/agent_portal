# app/api/v1/endpoints/logs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/{agent_id}", response_model=schemas.Log)
def create_log(
    agent_id: str,
    log: schemas.LogCreate,
    db: Session = Depends(get_db)
):
    """Create a new log entry for an agent"""
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_log = models.AgentLog(**log.dict(), agent_id=agent_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/{agent_id}", response_model=List[schemas.Log])
def get_logs(
    agent_id: str,
    level: str = None,
    category: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get logs for an agent"""
    query = db.query(models.AgentLog).filter(
        models.AgentLog.agent_id == agent_id,
        models.AgentLog.timestamp >= datetime.utcnow() - timedelta(hours=hours)
    )
    
    if level:
        query = query.filter(models.AgentLog.level == level)
    if category:
        query = query.filter(models.AgentLog.category == category)
    
    return query.order_by(models.AgentLog.timestamp.desc()).all()

@router.get("/", response_model=List[schemas.Log])
def get_all_logs(
    level: str = None,
    category: str = None,
    hours: int = 24,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get logs across all agents"""
    query = db.query(models.AgentLog).filter(
        models.AgentLog.timestamp >= datetime.utcnow() - timedelta(hours=hours)
    )
    
    if level:
        query = query.filter(models.AgentLog.level == level)
    if category:
        query = query.filter(models.AgentLog.category == category)
    
    return query.order_by(models.AgentLog.timestamp.desc()).limit(limit).all()

@router.delete("/{agent_id}/clear")
def clear_logs(
    agent_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Delete old logs for an agent"""
    deleted = db.query(models.AgentLog).filter(
        models.AgentLog.agent_id == agent_id,
        models.AgentLog.timestamp < datetime.utcnow() - timedelta(days=days)
    ).delete()
    
    db.commit()
    return {
        "status": "success",
        "message": f"Deleted {deleted} logs older than {days} days"
    }