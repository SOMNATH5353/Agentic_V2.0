from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    mobile = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, nullable=True)
    experience = Column(Integer, default=0)
    resume_text = Column(Text, nullable=False)
    resume_embedding = Column(JSONB)
    skills_extracted = Column(JSONB)  # Store extracted skills from resume
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    applications = relationship("Application", back_populates="candidate")
