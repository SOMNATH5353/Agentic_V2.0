"""
Quick script to add missing columns to jobs, candidates, and applications tables
Run this once: python add_skills_column.py
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        # Add skills_extracted column to jobs table
        conn.execute(text("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS skills_extracted JSONB"))
        print("✅ Successfully added skills_extracted column to jobs table")
        
        # Add skills_extracted column to candidates table
        conn.execute(text("ALTER TABLE candidates ADD COLUMN IF NOT EXISTS skills_extracted JSONB"))
        print("✅ Successfully added skills_extracted column to candidates table")
        
        # Add missing columns to applications table
        conn.execute(text("ALTER TABLE applications ADD COLUMN IF NOT EXISTS fraud_details JSONB"))
        print("✅ Successfully added fraud_details column to applications table")
        
        conn.execute(text("ALTER TABLE applications ADD COLUMN IF NOT EXISTS explanation JSONB"))
        print("✅ Successfully added explanation column to applications table")
        
        conn.execute(text("ALTER TABLE applications ADD COLUMN IF NOT EXISTS skill_match JSONB"))
        print("✅ Successfully added skill_match column to applications table")
        
        conn.execute(text("ALTER TABLE applications ADD COLUMN IF NOT EXISTS experience_details JSONB"))
        print("✅ Successfully added experience_details column to applications table")
        
        conn.commit()
        print("\n✅ All database updates completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("The columns might already exist, which is fine!")
