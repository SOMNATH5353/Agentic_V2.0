"""
Check what skills are stored in Candidate ID 5 (Srivatsav)
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, name, skills_extracted FROM candidates WHERE id = 5"))
    candidate = result.fetchone()
    
    if candidate:
        print("=" * 70)
        print(f"Candidate ID: {candidate[0]}")
        print(f"Name: {candidate[1]}")
        print(f"\nSkills Extracted (stored in DB):")
        
        if candidate[2]:
            skills = json.loads(json.dumps(candidate[2]))
            print(f"  Technical: {skills.get('technical_skills', [])}")
            print(f"  All: {skills.get('all_skills', [])}")
        else:
            print("  None stored")
        print("=" * 70)
    else:
        print("Candidate not found")
