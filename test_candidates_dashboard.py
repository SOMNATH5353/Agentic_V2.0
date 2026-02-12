"""
Test script for the new Candidates Dashboard endpoint
"""
import requests
from datetime import datetime

BASE_URL = "https://agentic-v2-0.onrender.com"
# BASE_URL = "http://127.0.0.1:8000"  # For local testing

def test_candidates_dashboard():
    """Test the comprehensive candidates dashboard endpoint"""
    
    print("=" * 70)
    print("Testing Candidates Dashboard Endpoint")
    print("=" * 70)
    
    # Test 1: Get all candidates
    print("\n1. Getting all candidates...")
    response = requests.get(f"{BASE_URL}/analytics/candidates/dashboard")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n📊 STATISTICS:")
        print(f"   Total Candidates: {data['statistics']['total_candidates']}")
        print(f"   Average Score: {data['statistics']['average_score']}")
        
        print("\n📈 BY STATUS:")
        for status, count in data['statistics']['by_status'].items():
            print(f"   {status.capitalize()}: {count}")
        
        print("\n🏆 BY TIER:")
        for tier, count in data['statistics']['by_tier'].items():
            print(f"   {tier.capitalize()}: {count}")
        
        print("\n✅ BY DECISION:")
        for decision, count in data['statistics']['by_decision'].items():
            print(f"   {decision.replace('_', ' ').title()}: {count}")
        
        print(f"\n👥 SHOWING {data['pagination']['showing']} candidates:")
        print("-" * 70)
        
        for i, candidate in enumerate(data['candidates'][:5], 1):  # Show first 5
            print(f"\n{i}. {candidate['candidate_name']} ({candidate['tier']} Tier)")
            print(f"   Email: {candidate['email']}")
            print(f"   Experience: {candidate['experience']} years")
            print(f"   Status: {candidate['status']}")
            print(f"   Decision: {candidate['decision']}")
            print(f"   Score: {candidate['scores']['percentage']} (Composite: {candidate['scores']['composite_score']})")
            print(f"   Applied for: {candidate['best_application']['job_role']}")
            print(f"   Company: {candidate['best_application']['company_name']}")
            print(f"   Rank: #{candidate['rank']}")
            print(f"   Total Applications: {candidate['total_applications']}")
            if candidate['fraud_flag']:
                print(f"   ⚠️  FRAUD FLAG DETECTED")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    # Test 2: Filter by Excellent tier
    print("\n\n" + "=" * 70)
    print("2. Getting only EXCELLENT tier candidates...")
    response = requests.get(
        f"{BASE_URL}/analytics/candidates/dashboard",
        params={"tier_filter": "Excellent"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} Excellent candidates")
        for candidate in data['candidates'][:3]:
            print(f"   • {candidate['candidate_name']}: {candidate['scores']['percentage']}")
    
    # Test 3: Filter by Selected status
    print("\n" + "=" * 70)
    print("3. Getting only SELECTED candidates...")
    response = requests.get(
        f"{BASE_URL}/analytics/candidates/dashboard",
        params={"status_filter": "Selected"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} Selected candidates")
        for candidate in data['candidates'][:3]:
            print(f"   • {candidate['candidate_name']}: {candidate['decision']} - {candidate['scores']['percentage']}")
    
    # Test 4: Combined filters
    print("\n" + "=" * 70)
    print("4. Getting Excellent + Selected candidates...")
    response = requests.get(
        f"{BASE_URL}/analytics/candidates/dashboard",
        params={
            "tier_filter": "Excellent",
            "status_filter": "Selected",
            "limit": 10
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['pagination']['total']} candidates matching both filters")
        for candidate in data['candidates']:
            print(f"   • {candidate['candidate_name']}: {candidate['scores']['percentage']} - {candidate['decision']}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)


def export_to_csv():
    """Export dashboard data to CSV for Excel analysis"""
    print("\n📥 Exporting candidates data to CSV...")
    
    response = requests.get(f"{BASE_URL}/analytics/candidates/dashboard", params={"limit": 1000})
    
    if response.status_code == 200:
        data = response.json()
        
        import csv
        
        filename = f"candidates_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Candidate ID', 'Name', 'Email', 'Mobile', 'Experience',
                'Job Role', 'Company', 'Score', 'Percentage',
                'Decision', 'Status', 'Tier', 'Rank', 'Fraud Flag',
                'RFS', 'DCS', 'ELC', 'Total Applications'
            ])
            
            # Data
            for c in data['candidates']:
                writer.writerow([
                    c['candidate_id'],
                    c['candidate_name'],
                    c['email'],
                    c['mobile'],
                    c['experience'],
                    c['best_application']['job_role'],
                    c['best_application']['company_name'],
                    c['scores']['composite_score'],
                    c['scores']['percentage'],
                    c['decision'],
                    c['status'],
                    c['tier'],
                    c['rank'],
                    'Yes' if c['fraud_flag'] else 'No',
                    c['scores']['rfs'],
                    c['scores']['dcs'],
                    c['scores']['elc'],
                    c['total_applications']
                ])
        
        print(f"✅ Exported {len(data['candidates'])} candidates to {filename}")
    else:
        print(f"❌ Error: {response.status_code}")


if __name__ == "__main__":
    test_candidates_dashboard()
    
    # Uncomment to export to CSV
    # export_to_csv()
