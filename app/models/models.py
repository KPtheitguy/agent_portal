# app/models/models.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    status = Column(String, default='registered')
    version = Column(String)
    os_info = Column(JSON, default={})
    last_seen = Column(DateTime, default=datetime.utcnow)
    registered_at = Column(DateTime, default=datetime.utcnow)
    config = Column(JSON, default={})
    tags = Column(JSON, default=[])

    # Relationships
    nginx_configs = relationship("NginxConfig", back_populates="agent", cascade="all, delete-orphan")
    logs = relationship("AgentLog", back_populates="agent", cascade="all, delete-orphan")
    metrics = relationship("AgentMetric", back_populates="agent", cascade="all, delete-orphan")

class NginxConfig(Base):
    __tablename__ = "nginx_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'))
    name = Column(String, nullable=False)
    config_type = Column(String, nullable=False)
    domain = Column(String)
    config = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="nginx_configs")
    ssl_cert = relationship("SSLCertificate", back_populates="nginx_config", uselist=False)

class SSLCertificate(Base):
    __tablename__ = "ssl_certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_id = Column(UUID(as_uuid=True), ForeignKey('nginx_configs.id'))
    domain = Column(String, nullable=False)
    issuer = Column(String)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)
    status = Column(String)
    auto_renewal = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    nginx_config = relationship("NginxConfig", back_populates="ssl_cert")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    category = Column(String)
    message = Column(String)
    details = Column(JSON)

    # Relationships
    agent = relationship("Agent", back_populates="logs")

class AgentMetric(Base):
    __tablename__ = "agent_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    metric_type = Column(String)
    value = Column(JSON)

    # Relationships
    agent = relationship("Agent", back_populates="metrics")