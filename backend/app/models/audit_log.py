from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    event_type = Column(String)  # application_evaluation, job_creation, fraud_detection, etc.
    entity_type = Column(String)  # application, job, candidate, company
    entity_id = Column(Integer)
    user_id = Column(Integer, nullable=True)
    action = Column(String)  # create, update, delete, evaluate, flag, override
    details = Column(Text)  # JSON string with detailed information
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
