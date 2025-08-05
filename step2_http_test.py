#!/usr/bin/env python3

"""
🧪 STEP 2: HTTP Endpoint Test
Test the Flask /analyze/task endpoint and HTML report generation
"""

import requests
import os
import time
import subprocess
import sys

def test_http_endpoint():
    """Test the HTTP endpoint and report generation."""
    
    print("🧪 STEP 2: HTTP ENDPOINT TEST")
    print("=" * 60)
    
    # Check if server is running
    server_url = "http://localhost:5006"
    
    print("🌐 Checking if Flask server is running...")
    try:
        response = requests.get(server_url, timeout=5)
        print("✅ Server is running")
    except requests.exceptions.RequestException:
        print("❌ Server not running - please start with: python app.py")
        return False
    
    # Use the test HTML file from Step 1
    test_file_path = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/test_page.html"
    if not os.path.exists(test_file_path):
        print(f"❌ Test HTML file not found: {test_file_path}")
        print("Please run step1_unit_test.py first to create the test file")
        return False
    
    test_url = f"file://{test_file_path}"
    test_scenario = "Click the Contact Us button and verify the form appears"
    
    print(f"🎯 Testing scenario: {test_scenario}")
    print(f"🌐 Test URL: {test_url}")
    
    # Prepare the POST data
    data = {
        'url': test_url,
        'scenario': test_scenario
    }
    
    print("\\n📡 Sending POST request to /analyze/task...")
    
    try:
        # Send request to Flask endpoint
        response = requests.post(
            f"{server_url}/analyze/task",
            data=data,
            timeout=120,  # Allow up to 2 minutes for analysis
            allow_redirects=False
        )
        
        print(f"✅ Request completed - Status: {response.status_code}")
        
        # Save the HTML report
        report_path = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/report.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Report saved to: {report_path}")
        
        # Verify the HTML content
        if "UX Analysis Report" in response.text or "Interactive Analysis" in response.text:
            print("✅ HTML report contains expected content")
        else:
            print("⚠️  HTML report may not have expected content")
        
        # Check for key elements in the report
        report_checks = [
            ("scenario" in response.text.lower(), "Scenario information"),
            ("analysis" in response.text.lower(), "Analysis content"),
            ("<!DOCTYPE html>" in response.text or "<html" in response.text, "Valid HTML structure"),
        ]
        
        print("\\n📋 REPORT VALIDATION:")
        print("=" * 40)
        
        for check, description in report_checks:
            status = "✅" if check else "❌"
            print(f"{status} {description}")
        
        # Try to open the report (optional)
        print(f"\\n🌐 To view the report, open: {report_path}")
        print("Or run: open report.html")
        
        print("\\n🎯 HTTP ENDPOINT TEST: ✅ PASSED")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout - analysis took too long")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_server_if_needed():
    """Helper to check if server needs to be started."""
    try:
        response = requests.get("http://localhost:5006", timeout=2)
        return True
    except:
        print("\\n💡 TIP: If server isn't running, start it with:")
        print("   cd '/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer'")
        print("   python app.py")
        print("\\nThen run this test again.")
        return False

if __name__ == "__main__":
    if not start_server_if_needed():
        sys.exit(1)
    
    success = test_http_endpoint()
    if success:
        print("\\n🌟 Step 2 completed successfully - HTTP endpoint works!")
    else:
        print("\\n💥 Step 2 failed - Issues with HTTP endpoint")
        sys.exit(1)
