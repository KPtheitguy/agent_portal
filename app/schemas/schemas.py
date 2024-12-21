# app/schemas/schemas.py
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, List, Any
from datetime import datetime

class TokenRequest(BaseModel):
    admin_key: str
    environment: str
    description: Optional[str] = None
    expiry_hours: Optional[int] = 24

class TokenResponse(BaseModel):
    token: str
    expires_at: datetime
    environment: str

class AgentRegister(BaseModel):
    hostname: str
    ip_address: str
    registration_token: str
    version: Optional[str] = None
    description: Optional[str] = None
    os_info: Optional[Dict] = {}

class Agent(BaseModel):
    id: UUID4
    hostname: str
    ip_address: str
    environment: str
    description: Optional[str]
    version: Optional[str]
    os_info: Dict
    status: str
    last_seen: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class AgentResponse(BaseModel):
    agent: Agent
    api_key: str

class MetricCreate(BaseModel):
    metric_type: str
    value: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()

class Metric(MetricCreate):
    id: UUID4
    agent_id: UUID4

    class Config:
        from_attributes = True

class MetricsSubmit(BaseModel):
    cpu: Dict
    memory: Dict
    disk: Dict
    network: Dict
    timestamp: datetime = datetime.utcnow()

class LogCreate(BaseModel):
    level: str
    message: str
    details: Optional[Dict] = None
    timestamp: datetime = datetime.utcnow()

class Log(LogCreate):
    id: UUID4
    agent_id: UUID4

    class Config:
        from_attributes = True

class LogSubmit(BaseModel):
    level: str
    message: str
    details: Optional[Dict] = None
    timestamp: datetime = datetime.utcnow()

class AgentUpdate(BaseModel):
    description: Optional[str]
    version: Optional[str]
    status: Optional[str]