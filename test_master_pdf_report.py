"""
Test script for Master PDF Report API endpoint
This tests the comprehensive PDF generation with all candidate analytics
"""

import requests
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
ENDPOINT = "/analytics/master-report/pdf"

def test_master_pdf_report():
    """Test the master PDF report generation endpoint"""
    
    print("🔍 Testing Master PDF Report Generation API")
    print("=" * 70)
    
    # Test parameters
    test_cases = [
        {"limit": 10, "skip": 0, "description": "First 10 candidates"},
        {"limit": 5, "skip": 0, "description": "First 5 candidates"},
        {"limit": 20, "skip": 0, "description": "First 20 candidates"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}: {test_case['description']}")
        print("-" * 70)
        
        params = {
            "limit": test_case["limit"],
            "skip": test_case["skip"]
        }
        
        try:
            # Make the request
            print(f"🔗 URL: {BASE_URL}{ENDPOINT}")
            print(f"📝 Parameters: {params}")
            print("⏳ Generating PDF report...")
            
            response = requests.get(
                f"{BASE_URL}{ENDPOINT}",
                params=params,
                stream=True,
                timeout=60  # 60 seconds timeout for large reports
            )
            
            # Check response
            if response.status_code == 200:
                print(f"✅ SUCCESS - Status Code: {response.status_code}")
                
                # Get content details
                content_type = response.headers.get('content-type', '')
                content_disposition = response.headers.get('content-disposition', '')
                content_length = response.headers.get('content-length', 'Unknown')
                
                print(f"📄 Content-Type: {content_type}")
                print(f"📎 Content-Disposition: {content_disposition}")
                print(f"💾 Content-Length: {content_length} bytes")
                
                # Save the PDF file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"master_report_{test_case['limit']}candidates_{timestamp}.pdf"
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = os.path.getsize(filename)
                print(f"💾 PDF saved as: {filename}")
                print(f"📊 File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
                
                # Verify it's a valid PDF
                with open(filename, 'rb') as f:
                    header = f.read(4)
                    if header == b'%PDF':
                        print("✅ Valid PDF file confirmed")
                    else:
                        print("⚠️  Warning: File may not be a valid PDF")
                
                print(f"\n📂 Open the PDF: {os.path.abspath(filename)}")
                
            else:
                print(f"❌ ERROR - Status Code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
        except requests.exceptions.ConnectionError:
            print("❌ ERROR: Could not connect to the server")
            print("Make sure the FastAPI server is running on http://localhost:8000")
        except requests.exceptions.Timeout:
            print("❌ ERROR: Request timed out (exceeded 60 seconds)")
            print("The report might be too large. Try reducing the limit parameter.")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🏁 Test completed!")
    print("\n📋 What the PDF should contain:")
    print("   ✓ Title page with report metadata")
    print("   ✓ Executive summary with statistics")
    print("   ✓ Top 5 performers ranking")
    print("   ✓ Individual candidate profiles")
    print("   ✓ Application details for each candidate")
    print("   ✓ Score visualizations (bar charts)")
    print("   ✓ XAI explanations")
    print("   ✓ Skill gap analysis")
    print("   ✓ Skill match evidence")
    print("   ✓ Fraud detection results")


def test_edge_cases():
    """Test edge cases and error handling"""
    
    print("\n\n🧪 Testing Edge Cases")
    print("=" * 70)
    
    edge_cases = [
        {"limit": 0, "skip": 0, "description": "Zero limit"},
        {"limit": 150, "skip": 0, "description": "Limit exceeding maximum (should cap at 100)"},
        {"limit": 10, "skip": 1000, "description": "Large skip value (no candidates)"},
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n🔬 Edge Case {i}: {test_case['description']}")
        print("-" * 70)
        
        params = {
            "limit": test_case["limit"],
            "skip": test_case["skip"]
        }
        
        try:
            response = requests.get(
                f"{BASE_URL}{ENDPOINT}",
                params=params,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Request succeeded (limit={test_case['limit']}, skip={test_case['skip']})")
                content_length = response.headers.get('content-length', 'Unknown')
                print(f"Content-Length: {content_length} bytes")
            elif response.status_code == 404:
                print(f"✅ Expected 404 - No candidates found")
            else:
                print(f"Response: {response.text[:300]}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Master PDF Report API - Test Suite")
    print("=" * 70)
    print("This script tests the comprehensive PDF generation endpoint")
    print("that combines rankings, XAI, skill gaps, and visualizations")
    print("=" * 70)
    
    # Run main tests
    test_master_pdf_report()
    
    # Run edge case tests
    test_edge_cases()
    
    print("\n\n✅ All tests completed!")
    print("Check the generated PDF files in the current directory")
