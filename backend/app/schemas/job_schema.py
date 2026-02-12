from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobBase(BaseModel):
    role: str
    location: Optional[str] = None
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    required_experience: int = 0


class JobCreate(JobBase):
    company_id: int


class JobListResponse(BaseModel):
    id: int
    company_id: int
    role: str
    location: Optional[str] = None
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    required_experience: int
    created_at: datetime
    company_name: Optional[str] = None  # Will be populated from company relation
    application_count: int = 0
    
    class Config:
        from_attributes = True


class JobDetailResponse(JobBase):
    id: int
    company_id: int
    jd_text: str
    created_at: datetime
    skills_extracted: Optional[dict] = None
    company_name: Optional[str] = None
    
    class Config:
        from_attributes = True
