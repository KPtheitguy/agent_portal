# app/schemas/schemas.py
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, List, Any
from datetime import datetime

class TokenRequest(BaseModel):
    environment: str
    description: Optional[str] = None
    expiry_hours: Optional[int] = 24

class TokenResponse(BaseModel):
    token: str
    expires_at: datetime

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

# Add Metric schemas
class MetricBase(BaseModel):
    metric_type: str
    value: Dict[str, Any]
    timestamp: Optional[datetime] = None

class MetricCreate(MetricBase):
    agent_id: UUID4

class Metric(MetricBase):
    id: UUID4
    agent_id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricsSubmit(BaseModel):
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk: Dict[str, Any]
    network: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()

# Log schemas
class LogBase(BaseModel):
    level: str
    message: str
    details: Optional[Dict] = None
    timestamp: Optional[datetime] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: UUID4
    agent_id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class LogSubmit(BaseModel):
    level: str
    message: str
    details: Optional[Dict] = None
    timestamp: datetime = datetime.utcnow()