"""
Migration script to add rank column to applications table
Run this after updating models to add rank column for application rankings
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
    """Add rank column to applications table"""
    
    with engine.connect() as conn:
        try:
            # Add rank column to applications table if it doesn't exist
            print("Adding rank column to applications table...")
            conn.execute(text("""
                ALTER TABLE applications 
                ADD COLUMN IF NOT EXISTS rank INTEGER;
            """))
            conn.commit()
            print("✓ Rank column added to applications table")
            
            # Create index on rank for better query performance
            print("Creating index on rank column...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_applications_rank 
                ON applications(rank);
            """))
            conn.commit()
            print("✓ Index created on rank column")
            
            print("\n✓ Migration completed successfully!")
            print("\nNext step: Rankings will be automatically calculated when new applications are submitted.")
            print("To calculate rankings for existing applications, restart the application evaluation process.")
            
        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("Starting database migration for ranking feature...")
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}\n")
    
    response = input("Do you want to proceed with the migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        run_migration()
    else:
        print("Migration cancelled")
