"""
Test script for the merged endpoint: Create Company + Job in one API call
"""
import requests

# Base URL
BASE_URL = "https://agentic-v2-0.onrender.com"

def test_create_job_with_company():
    """
    Test the merged endpoint that creates both company and job
    """
    url = f"{BASE_URL}/job/create-with-company"
    
    # Prepare form data
    data = {
        # Company details
        "company_name": "TechCorp Solutions",
        "company_description": "Leading AI and Machine Learning company specializing in innovative solutions",
        
        # Job details
        "role": "Senior Python Developer",
        "location": "Remote (US/Europe)",
        "salary": "$100k-$150k",
        "employment_type": "Full-time",
        "required_experience": 3
    }
    
    # Prepare file (make sure you have a JD PDF file)
    try:
        with open("job_description.pdf", "rb") as f:
            files = {"jd_pdf": f}
            
            print("🚀 Sending request to create company and job...")
            response = requests.post(url, data=data, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ SUCCESS!\n")
                
                print("📌 Company Details:")
                print(f"   ID: {result['company']['id']}")
                print(f"   Name: {result['company']['name']}")
                print(f"   Status: {result['company']['status']}")
                print(f"   Created: {result['company']['created_at']}")
                
                print("\n📌 Job Details:")
                print(f"   ID: {result['job']['id']}")
                print(f"   Role: {result['job']['role']}")
                print(f"   Location: {result['job']['location']}")
                print(f"   Salary: {result['job']['salary']}")
                print(f"   Employment Type: {result['job']['employment_type']}")
                
                print(f"\n📊 Skills Extracted: {len(result['skills_extracted'])} skills")
                print(f"   Technical Skills: {', '.join(result['technical_skills'])}")
                print(f"   Soft Skills: {', '.join(result['soft_skills'])}")
                
                print(f"\n💬 Message: {result['message']}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.json())
                
    except FileNotFoundError:
        print("❌ Error: job_description.pdf not found!")
        print("Please create a job description PDF file first.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_health_check():
    """Test if the API is reachable"""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ API is healthy:", response.json())
            return True
        else:
            print("❌ API health check failed")
            return False
    except Exception as e:
        print(f"❌ Cannot reach API: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Merged Endpoint: Create Company + Job")
    print("=" * 60)
    
    # First check if API is accessible
    print("\n1. Checking API health...")
    if test_health_check():
        print("\n2. Testing merged endpoint...")
        test_create_job_with_company()
    else:
        print("\n⚠️  API is not accessible. Please check the deployment.")
    
    print("\n" + "=" * 60)
