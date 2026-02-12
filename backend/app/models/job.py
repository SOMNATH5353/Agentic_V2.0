from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    role = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    salary = Column(String)
    employment_type = Column(String, nullable=True)  # Full-time, Part-time, Contract, etc.
    required_experience = Column(Integer, default=0)
    jd_text = Column(Text, nullable=False)
    jd_embedding = Column(JSONB)
    skills_extracted = Column(JSONB)  # Store extracted skills from JD
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
