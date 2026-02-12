"""
Quick migration script to add new columns (auto-runs without confirmation)
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
            # Add mobile column to candidates table
            print("Adding mobile column to candidates table...")
            conn.execute(text("""
                ALTER TABLE candidates 
                ADD COLUMN IF NOT EXISTS mobile VARCHAR;
            """))
            conn.commit()
            print("✓ Mobile column added")
            
            # Add location column to jobs table
            print("Adding location column to jobs table...")
            conn.execute(text("""
                ALTER TABLE jobs 
                ADD COLUMN IF NOT EXISTS location VARCHAR;
            """))
            conn.commit()
            print("✓ Location column added")
            
            # Add employment_type column to jobs table
            print("Adding employment_type column to jobs table...")
            conn.execute(text("""
                ALTER TABLE jobs 
                ADD COLUMN IF NOT EXISTS employment_type VARCHAR;
            """))
            conn.commit()
            print("✓ Employment_type column added")
            
            # Add rank column to applications table
            print("Adding rank column to applications table...")
            conn.execute(text("""
                ALTER TABLE applications 
                ADD COLUMN IF NOT EXISTS rank INTEGER;
            """))
            conn.commit()
            print("✓ Rank column added")
            
            # Create index on rank
            print("Creating index on rank column...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_applications_rank 
                ON applications(rank);
            """))
            conn.commit()
            print("✓ Index created")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("Running database migration...")
    run_migration()
