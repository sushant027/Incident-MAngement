from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean, default=True)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    exception_text = Column(Text, nullable=True)
    bank_id = Column(Integer)
    severity = Column(String)
    status = Column(String, default="OPEN")
    service_name = Column(String)
    incident_manager = Column(Integer)
    current_owner = Column(Integer)
    created_by = Column(Integer)
    source = Column(String)
    impact_summary = Column(Text)
    downtime = Column(Boolean, nullable=True)
    financial_impact = Column(Boolean, nullable=True)
    technical_decline_pct = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

class IncidentTimeline(Base):
    __tablename__ = "incident_timeline"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer)
    action = Column(String)
    details = Column(Text)
    created_by = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class CorrectiveAction(Base):
    __tablename__ = "corrective_actions"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer)
    title = Column(String)
    description = Column(Text)
    owner_user_id = Column(Integer)
    due_date = Column(Date)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    entity_type = Column(String)
    entity_id = Column(Integer)
    action = Column(String)
    performed_by = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
