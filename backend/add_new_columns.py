"""
Migration script to add new columns to existing tables
Run this after updating models to add:
- mobile column to candidates table
- location and employment_type columns to jobs table
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    exit(1)

engine = create_engine(DATABASE_URL)

def run_migration():
    """Add new columns to existing tables"""
    
    with engine.connect() as conn:
        try:
            # Add mobile column to candidates table if it doesn't exist
            print("Adding mobile column to candidates table...")
            conn.execute(text("""
                ALTER TABLE candidates 
                ADD COLUMN IF NOT EXISTS mobile VARCHAR;
            """))
            conn.commit()
            print("✓ Mobile column added to candidates table")
            
            # Add location column to jobs table if it doesn't exist
            print("Adding location column to jobs table...")
            conn.execute(text("""
                ALTER TABLE jobs 
                ADD COLUMN IF NOT EXISTS location VARCHAR;
            """))
            conn.commit()
            print("✓ Location column added to jobs table")
            
            # Add employment_type column to jobs table if it doesn't exist
            print("Adding employment_type column to jobs table...")
            conn.execute(text("""
                ALTER TABLE jobs 
                ADD COLUMN IF NOT EXISTS employment_type VARCHAR;
            """))
            conn.commit()
            print("✓ Employment_type column added to jobs table")
            
            print("\n✓ Migration completed successfully!")
            
        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("Starting database migration...")
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}\n")
    
    response = input("Do you want to proceed with the migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        run_migration()
    else:
        print("Migration cancelled")
