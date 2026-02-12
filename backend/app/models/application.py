from sqlalchemy import Column, Integer, Float, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)

    # Scores
    rfs = Column(Float)  # Role Fit Score
    dcs = Column(Float)  # Domain Competency Score
    elc = Column(Float)  # Experience Level Compatibility
    composite_score = Column(Float, index=True)
    
    # Ranking
    rank = Column(Integer, nullable=True, index=True)  # Rank among all applicants for this job

    # Fraud Detection
    similarity_index = Column(Float)
    fraud_flag = Column(Boolean, default=False, index=True)
    fraud_details = Column(JSONB, nullable=True)

    # Decision
    decision = Column(String, index=True)
    decision_reason = Column(Text)
    explanation = Column(JSONB, nullable=True)  # Store detailed explanation

    # Status
    status = Column(String, default="evaluated", index=True)
    
    # Additional Details
    skill_match = Column(JSONB, nullable=True)  # Store skill matching details
    experience_details = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
