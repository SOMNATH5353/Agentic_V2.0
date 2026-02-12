"""
Test script for the All Candidates Master Endpoint
Tests the /candidate/master/all endpoint
"""

import requests
import json

# Base URL - adjust if your server runs on a different port
BASE_URL = "http://localhost:8000"

def test_all_candidates_master(skip: int = 0, limit: int = 10):
    """
    Test the master endpoint for all candidates
    """
    print(f"\n{'='*80}")
    print(f"Testing All Candidates Master Endpoint")
    print(f"{'='*80}\n")
    
    # Make the request
    url = f"{BASE_URL}/candidate/master/all"
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        print(f"Requesting: {url}")
        print(f"Parameters: skip={skip}, limit={limit}")
        print("\nFetching data...\n")
        
        response = requests.get(url, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s\n")
        
        if response.status_code == 200:
            data = response.json()
            
            # Display pagination info
            print("📊 PAGINATION INFO:")
            print("-" * 80)
            print(f"Total Candidates in System: {data.get('total_candidates')}")
            print(f"Showing: {data.get('showing')} candidates")
            print(f"Skip: {data.get('skip')}")
            print(f"Limit: {data.get('limit')}")
            
            # Display global statistics
            print(f"\n📈 GLOBAL STATISTICS:")
            print("-" * 80)
            stats = data.get("global_statistics", {})
            print(f"Total Applications: {stats.get('total_applications')}")
            print(f"✅ Total Selected: {stats.get('total_selected')}")
            print(f"❌ Total Rejected: {stats.get('total_rejected')}")
            print(f"⏳ Total Pending: {stats.get('total_pending')}")
            
            # Display candidates
            candidates = data.get("candidates", [])
            print(f"\n👥 CANDIDATES ({len(candidates)}):")
            print("=" * 80)
            
            if not candidates:
                print("No candidates found in the system.")
            else:
                for idx, candidate_data in enumerate(candidates, 1):
                    profile = candidate_data.get("candidate_profile", {})
                    summary = candidate_data.get("application_summary", {})
                    
                    print(f"\n{idx}. {profile.get('name')} (ID: {profile.get('candidate_id')})")
                    print("-" * 80)
                    print(f"   Email: {profile.get('email')}")
                    print(f"   Mobile: {profile.get('mobile')}")
                    print(f"   Experience: {profile.get('years_of_experience')} years")
                    print(f"   Skills: {', '.join(profile.get('skills', [])[:5])}...")
                    
                    print(f"\n   📊 Application Summary:")
                    print(f"      Total Applications: {summary.get('total_applications')}")
                    print(f"      Selected: {summary.get('selected')}")
                    print(f"      Rejected: {summary.get('rejected')}")
                    print(f"      Pending: {summary.get('pending')}")
                    print(f"      Avg Score: {summary.get('average_composite_score')}")
                    
                    if summary.get('best_application'):
                        best = summary['best_application']
                        print(f"\n   🏆 Best Application:")
                        print(f"      Role: {best.get('job_role')}")
                        print(f"      Score: {best.get('composite_score')}")
                        print(f"      Decision: {best.get('decision')}")
                        print(f"      Rank: #{best.get('rank')}")
                    
                    applications = candidate_data.get("applications", [])
                    print(f"\n   📝 Applications: {len(applications)} total")
                    
                    # Show first 3 applications briefly
                    for app_idx, app in enumerate(applications[:3], 1):
                        job = app.get("job_details", {})
                        scores = app.get("scores", {})
                        decision = app.get("decision", {})
                        print(f"      {app_idx}. {job.get('role')} - Score: {scores.get('composite_score')} - {decision.get('status')}")
                    
                    if len(applications) > 3:
                        print(f"      ... and {len(applications) - 3} more applications")
            
            # Save full response to file
            filename = f"all_candidates_master_response.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full response saved to: {filename}")
            
            # Pagination suggestions
            total = data.get('total_candidates', 0)
            current_skip = data.get('skip', 0)
            current_limit = data.get('limit', 0)
            showing = data.get('showing', 0)
            
            if total > current_skip + showing:
                next_skip = current_skip + current_limit
                print(f"\n📄 More candidates available!")
                print(f"   To get next page, use: skip={next_skip}&limit={current_limit}")
            else:
                print(f"\n✅ All candidates retrieved!")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the server")
        print(f"   Make sure the server is running at {BASE_URL}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print(f"\n{'='*80}\n")


def test_export_all_candidates():
    """
    Export all candidates by fetching in batches
    """
    print("\n" + "="*80)
    print("EXPORTING ALL CANDIDATES")
    print("="*80)
    
    all_candidates = []
    skip = 0
    limit = 100
    
    try:
        while True:
            print(f"\nFetching batch: skip={skip}, limit={limit}...")
            url = f"{BASE_URL}/candidate/master/all"
            params = {"skip": skip, "limit": limit}
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                break
            
            data = response.json()
            candidates = data.get("candidates", [])
            
            if not candidates:
                break
            
            all_candidates.extend(candidates)
            print(f"Retrieved {len(candidates)} candidates. Total so far: {len(all_candidates)}")
            
            # Check if we got all candidates
            if len(candidates) < limit:
                break
            
            skip += limit
        
        # Save all candidates
        if all_candidates:
            filename = "all_candidates_complete_export.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_candidates": len(all_candidates),
                    "candidates": all_candidates
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Export Complete!")
            print(f"   Total candidates exported: {len(all_candidates)}")
            print(f"   Saved to: {filename}")
        else:
            print("\n⚠️  No candidates found in the system.")
            
    except Exception as e:
        print(f"❌ Error during export: {str(e)}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ALL CANDIDATES MASTER ENDPOINT TESTER")
    print("="*80)
    
    print("\nOptions:")
    print("1. Test with pagination (quick view)")
    print("2. Export all candidates (complete export)")
    
    choice = input("\nSelect option (1 or 2, default: 1): ").strip()
    
    if choice == "2":
        test_export_all_candidates()
    else:
        # Test with pagination
        skip_input = input("\nEnter skip value (default: 0): ").strip()
        limit_input = input("Enter limit value (default: 10): ").strip()
        
        skip = int(skip_input) if skip_input else 0
        limit = int(limit_input) if limit_input else 10
        
        test_all_candidates_master(skip, limit)
