"""
Script to delete test applications for re-testing
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("DELETE TEST APPLICATIONS")
print("=" * 70)

with engine.connect() as conn:
    # Show current applications
    result = conn.execute(text("""
        SELECT a.id, a.job_id, c.name, c.email, a.decision, a.composite_score
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        ORDER BY a.id DESC
        LIMIT 10
    """))
    
    applications = result.fetchall()
    
    if applications:
        print("\n📋 Current Applications:")
        print("-" * 70)
        for app in applications:
            print(f"ID: {app[0]} | Job: {app[1]} | {app[2]} ({app[3]}) | {app[4]} | Score: {app[5]:.2f}")
        
        print("\n" + "=" * 70)
        app_id = input("Enter Application ID to delete (or 'all' to delete all test apps): ")
        
        if app_id.lower() == 'all':
            confirm = input("⚠️  Delete ALL applications? (yes/no): ")
            if confirm.lower() == 'yes':
                conn.execute(text("DELETE FROM applications"))
                conn.commit()
                print("✅ All applications deleted")
            else:
                print("❌ Cancelled")
        else:
            try:
                app_id_int = int(app_id)
                conn.execute(text(f"DELETE FROM applications WHERE id = {app_id_int}"))
                conn.commit()
                print(f"✅ Application {app_id_int} deleted")
            except ValueError:
                print("❌ Invalid ID")
    else:
        print("\n✅ No applications found")
