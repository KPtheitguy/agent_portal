# app/api/v1/endpoints/metrics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/{agent_id}", response_model=schemas.Metric)
def record_metric(
    agent_id: str,
    metric: schemas.MetricCreate,
    db: Session = Depends(get_db)
):
    """Record a new metric for an agent"""
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_metric = models.AgentMetric(**metric.dict(), agent_id=agent_id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/{agent_id}", response_model=List[schemas.Metric])
def get_metrics(
    agent_id: str,
    metric_type: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get metrics for an agent"""
    query = db.query(models.AgentMetric).filter(
        models.AgentMetric.agent_id == agent_id,
        models.AgentMetric.timestamp >= datetime.utcnow() - timedelta(hours=hours)
    )
    
    if metric_type:
        query = query.filter(models.AgentMetric.metric_type == metric_type)
    
    return query.order_by(models.AgentMetric.timestamp.desc()).all()

@router.get("/{agent_id}/latest", response_model=schemas.Metric)
def get_latest_metric(
    agent_id: str,
    metric_type: str,
    db: Session = Depends(get_db)
):
    """Get latest metric of specific type for an agent"""
    metric = db.query(models.AgentMetric).filter(
        models.AgentMetric.agent_id == agent_id,
        models.AgentMetric.metric_type == metric_type
    ).order_by(models.AgentMetric.timestamp.desc()).first()
    
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    return metric

@router.delete("/{agent_id}")
def delete_old_metrics(
    agent_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Delete metrics older than specified days"""
    db.query(models.AgentMetric).filter(
        models.AgentMetric.agent_id == agent_id,
        models.AgentMetric.timestamp < datetime.utcnow() - timedelta(days=days)
    ).delete()
    
    db.commit()
    return {"status": "success", "message": f"Deleted metrics older than {days} days"}