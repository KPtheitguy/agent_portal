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

# CORS
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
    db: Session = Depends(get_db),
    admin_key: str = Depends(security.validate_admin_key)
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

# Agent routes
app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["agents"],
    dependencies=[Depends(security.validate_api_key)]
)

# Metrics routes
app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["metrics"],
    dependencies=[Depends(security.validate_api_key)]
)

# Logs routes
app.include_router(
    logs.router,
    prefix="/api/v1/logs",
    tags=["logs"],
    dependencies=[Depends(security.validate_api_key)]
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)