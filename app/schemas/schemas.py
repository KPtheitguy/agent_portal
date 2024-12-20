# app/schemas/schemas.py
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, List, Any
from datetime import datetime

class AgentBase(BaseModel):
    hostname: str
    ip_address: str
    version: Optional[str] = None
    os_info: Optional[Dict] = {}

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    status: Optional[str]
    config: Optional[Dict]
    tags: Optional[List[str]]

class Agent(AgentBase):
    id: UUID4
    status: str
    last_seen: datetime
    registered_at: datetime
    config: Dict = {}
    tags: List[str] = []

    class Config:
        from_attributes = True

class MetricCreate(BaseModel):
    metric_type: str
    value: Dict[str, Any]

class Metric(MetricCreate):
    id: UUID4
    agent_id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class LogCreate(BaseModel):
    level: str
    category: str
    message: str
    details: Optional[Dict] = None

class Log(LogCreate):
    id: UUID4
    agent_id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class NginxConfigCreate(BaseModel):
    name: str
    config_type: str
    domain: Optional[str]
    config: Dict[str, Any]

class NginxConfig(NginxConfigCreate):
    id: UUID4
    agent_id: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True