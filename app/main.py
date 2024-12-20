# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .api.v1.endpoints import agents, metrics, logs
from .core.database import engine, Base, get_db
from .schemas import schemas
from .config.settings import get_settings
from .core import security

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ubuntu Agent Manager",
    description="Management system for Ubuntu agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registration endpoints
@app.post("/api/v1/register/token", response_model=schemas.TokenResponse)
async def create_registration_token(
    request: schemas.TokenRequest,
    db: Session = Depends(get_db)
):
    """Generate a new registration token"""
    return await agents.get_registration_token(request, db)

@app.post("/api/v1/register/agent", response_model=schemas.AgentResponse)
async def register_agent(
    agent: schemas.AgentRegister,
    db: Session = Depends(get_db)
):
    """Register a new agent"""
    return await agents.register_agent(agent, db)

@app.get("/api/v1/agents", response_model=List[schemas.Agent])
async def list_agents(
    environment: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_admin_key)
):
    """List all registered agents"""
    return await agents.get_agents(environment, status, db)

@app.get("/api/v1/agents/{agent_id}", response_model=schemas.Agent)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_api_key)
):
    """Get agent details"""
    return await agents.get_agent(agent_id, db)

@app.post("/api/v1/agents/{agent_id}/metrics")
async def submit_metrics(
    agent_id: str,
    metrics: schemas.MetricsSubmit,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_api_key)
):
    """Submit agent metrics"""
    return await metrics.submit_metrics(agent_id, metrics, db)

@app.post("/api/v1/agents/{agent_id}/logs")
async def submit_logs(
    agent_id: str,
    logs: schemas.LogSubmit,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_api_key)
):
    """Submit agent logs"""
    return await logs.submit_logs(agent_id, logs, db)

@app.delete("/api/v1/agents/{agent_id}")
async def deregister_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_admin_key)
):
    """Deregister an agent"""
    return await agents.deregister_agent(agent_id, db)

@app.post("/api/v1/agents/{agent_id}/revoke")
async def revoke_agent_key(
    agent_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.validate_admin_key)
):
    """Revoke agent's API key"""
    return await agents.revoke_agent_key(agent_id, db)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

# Include other routers
app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["agents"]
)

app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["metrics"]
)

app.include_router(
    logs.router,
    prefix="/api/v1/logs",
    tags=["logs"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)