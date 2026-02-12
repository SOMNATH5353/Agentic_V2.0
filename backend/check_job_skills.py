"""
Check what skills are stored in Job ID 4
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, role, skills_extracted FROM jobs WHERE id = 4"))
    job = result.fetchone()
    
    if job:
        print("=" * 70)
        print(f"Job ID: {job[0]}")
        print(f"Role: {job[1]}")
        print(f"\nSkills Extracted (stored in DB):")
        
        if job[2]:
            skills = json.loads(json.dumps(job[2]))
            print(f"  Technical: {skills.get('technical_skills', [])}")
            print(f"  All: {skills.get('all_skills', [])}")
        else:
            print("  None stored")
        print("=" * 70)
    else:
        print("Job not found")
