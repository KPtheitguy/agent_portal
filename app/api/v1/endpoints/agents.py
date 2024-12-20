# app/api/v1/endpoints/agents.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas import schemas
from ....models import models
from datetime import datetime

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}}
)

@router.post("/register", response_model=schemas.Agent, 
            summary="Register a new agent",
            description="Register a new agent or update existing one")
def register_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    try:
        existing_agent = db.query(models.Agent).filter(
            models.Agent.hostname == agent.hostname
        ).first()

        if existing_agent:
            for key, value in agent.dict(exclude_unset=True).items():
                setattr(existing_agent, key, value)
            existing_agent.last_seen = datetime.utcnow()
            existing_agent.status = 'active'
            db.commit()
            db.refresh(existing_agent)
            return existing_agent

        db_agent = models.Agent(**agent.dict())
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Agent],
           summary="List all agents",
           description="Get a list of all registered agents with optional status filter")
def list_agents(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Agent)
    if status:
        query = query.filter(models.Agent.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{agent_id}", response_model=schemas.Agent,
           summary="Get agent details",
           description="Get detailed information about a specific agent")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=schemas.Agent,
           summary="Update agent",
           description="Update agent information")
def update_agent(
    agent_id: str,
    agent_update: schemas.AgentUpdate,
    db: Session = Depends(get_db)
):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    for key, value in agent_update.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)

    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.delete("/{agent_id}",
              summary="Delete agent",
              description="Delete an agent from the system")
def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    return {"status": "success", "message": "Agent deleted"}