"""
Test script for the Candidate Master Endpoint
Tests the /candidate/{candidate_id}/master endpoint
"""

import requests
import json

# Base URL - adjust if your server runs on a different port
BASE_URL = "http://localhost:8000"

def test_master_endpoint(candidate_id: int):
    """
    Test the master endpoint for a specific candidate
    """
    print(f"\n{'='*80}")
    print(f"Testing Master Endpoint for Candidate ID: {candidate_id}")
    print(f"{'='*80}\n")
    
    # Make the request
    url = f"{BASE_URL}/candidate/{candidate_id}/master"
    
    try:
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s\n")
        
        if response.status_code == 200:
            data = response.json()
            
            # Display Candidate Profile
            print("📋 CANDIDATE PROFILE:")
            print("-" * 80)
            profile = data.get("candidate_profile", {})
            print(f"Name: {profile.get('name')}")
            print(f"Email: {profile.get('email')}")
            print(f"Mobile: {profile.get('mobile')}")
            print(f"LinkedIn: {profile.get('linkedin')}")
            print(f"GitHub: {profile.get('github')}")
            print(f"Experience: {profile.get('years_of_experience')} years")
            print(f"Skills: {', '.join(profile.get('skills', []))}")
            print(f"Profile Created: {profile.get('profile_created_at')}")
            
            # Display Application Summary
            print(f"\n📊 APPLICATION SUMMARY:")
            print("-" * 80)
            summary = data.get("application_summary", {})
            print(f"Total Applications: {summary.get('total_applications')}")
            print(f"✅ Selected: {summary.get('selected')}")
            print(f"❌ Rejected: {summary.get('rejected')}")
            print(f"⏳ Pending: {summary.get('pending')}")
            print(f"Average Composite Score: {summary.get('average_composite_score')}")
            
            if summary.get('best_application'):
                best = summary['best_application']
                print(f"\n🏆 Best Application:")
                print(f"   Role: {best.get('job_role')}")
                print(f"   Score: {best.get('composite_score')}")
                print(f"   Rank: #{best.get('rank')}")
                print(f"   Decision: {best.get('decision')}")
            
            # Display Applications
            applications = data.get("applications", [])
            print(f"\n📝 DETAILED APPLICATIONS ({len(applications)}):")
            print("=" * 80)
            
            for idx, app in enumerate(applications, 1):
                print(f"\nApplication #{idx} (ID: {app.get('application_id')})")
                print("-" * 80)
                
                # Job details
                job = app.get("job_details", {})
                print(f"Role: {job.get('role')}")
                print(f"Location: {job.get('location')}")
                print(f"Salary: {job.get('salary')}")
                print(f"Type: {job.get('employment_type')}")
                
                # Company details
                company = app.get("company_details", {})
                if company:
                    print(f"Company: {company.get('company_name')}")
                
                # Scores
                scores = app.get("scores", {})
                print(f"\n📈 Scores:")
                print(f"   Role Fit Score: {scores.get('role_fit_score')}")
                print(f"   Domain Competency: {scores.get('domain_competency_score')}")
                print(f"   Experience Compatibility: {scores.get('experience_level_compatibility')}")
                print(f"   Composite Score: {scores.get('composite_score')}")
                print(f"   Rank: {scores.get('rank_description')}")
                
                # Decision
                decision = app.get("decision", {})
                print(f"\n🎯 Decision: {decision.get('status')}")
                if decision.get('reason'):
                    print(f"   Reason: {decision.get('reason')}")
                
                # Fraud Detection
                fraud = app.get("fraud_detection", {})
                if fraud.get('fraud_flag'):
                    print(f"\n⚠️  FRAUD DETECTED!")
                    print(f"   Similarity Index: {fraud.get('similarity_index')}")
                else:
                    print(f"\n✅ No fraud detected (Similarity: {fraud.get('similarity_index')})")
            
            # Save full response to file
            filename = f"candidate_{candidate_id}_master_response.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full response saved to: {filename}")
            
        elif response.status_code == 404:
            print(f"❌ Candidate with ID {candidate_id} not found")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the server")
        print(f"   Make sure the server is running at {BASE_URL}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("CANDIDATE MASTER ENDPOINT TESTER")
    print("="*80)
    
    # Test with candidate ID 1 (you can change this)
    candidate_id = input("\nEnter Candidate ID to test (default: 1): ").strip()
    
    if not candidate_id:
        candidate_id = 1
    else:
        try:
            candidate_id = int(candidate_id)
        except ValueError:
            print("Invalid candidate ID. Using default: 1")
            candidate_id = 1
    
    test_master_endpoint(candidate_id)
