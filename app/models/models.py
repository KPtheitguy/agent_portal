# app/models/models.py

from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..core.database import Base

class RegistrationToken(Base):
    __tablename__ = "registration_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, unique=True, nullable=False)
    environment = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    used_by = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=True)
    used_at = Column(DateTime, nullable=True)

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    description = Column(String)
    version = Column(String)
    os_info = Column(JSON)
    status = Column(String, default='registered')
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentApiKey(Base):
    __tablename__ = "agent_api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=False)
    key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)