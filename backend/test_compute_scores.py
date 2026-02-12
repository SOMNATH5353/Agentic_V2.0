"""
Test the compute_all_scores function with database records
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Import all models first to ensure relationships workfrom app.database import Base
from app.models.company import Company
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.application import Application
from app.services.scoring_engine import compute_all_scores

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Get Job ID 4
    job = db.query(Job).filter(Job.id == 4).first()
    if not job:
        print("ERROR: Job 4 not found")
        exit(1)
    
    print(f"Job ID: {job.id}")
    print(f"Job has skills_extracted: {hasattr(job, 'skills_extracted')}")
    print(f"Job skills_extracted value: {job.skills_extracted}")
    print(f"Job skills_extracted type: {type(job.skills_extracted)}")
    
    # Get Candidate ID 5
    candidate = db.query(Candidate).filter(Candidate.id == 5).first()
    if not candidate:
        print("ERROR: Candidate 5 not found")
        exit(1)
    
    print(f"\nCandidate ID: {candidate.id}")
    print(f"Candidate has skills_extracted: {hasattr(candidate, 'skills_extracted')}")
    print(f"Candidate skills_extracted value: {candidate.skills_extracted}")
    print(f"Candidate skills_extracted type: {type(candidate.skills_extracted)}")
    
    print("\n" + "="*70)
    print("Testing compute_all_scores...")
    print("="*70)
    
    result = compute_all_scores(job, candidate)
    
    print("\nSUCCESS!")
    print(f"RFS: {result['rfs']}")
    print(f"DCS: {result['dcs']}")
    print(f"ELC: {result['elc']}")
    print(f"Composite: {result['composite_score']}")
    print(f"Skill Match %: {result['skill_match']['match_percentage']}")
    print(f"Matched Skills: {result['skill_match']['matched_skills']}")
    print(f"Missing Skills: {result['skill_match']['missing_skills']}")
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
