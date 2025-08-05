#!/usr/bin/env python3
"""
🔍 Server Connectivity Test
Quick verification that server and mocks are accessible
"""

import requests
import time

def test_connectivity():
    print("🔍 SERVER CONNECTIVITY TEST")
    print("=" * 30)
    
    # Test server health
    try:
        print("📡 Testing server health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server health check passed!")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"⚠️ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on localhost:8000")
        print("💡 Make sure the server is running in another terminal!")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test each Office mock
    mocks = [
        ("📄 Word Mock", "word.html"),
        ("📊 Excel Mock", "excel.html"), 
        ("📑 PowerPoint Mock", "powerpoint.html")
    ]
    
    print("\n🌐 Testing Office Mocks...")
    all_good = True
    
    for name, filename in mocks:
        try:
            url = f"http://localhost:8000/mocks/{filename}"
            print(f"Testing {name}...")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                content_length = len(response.text)
                print(f"✅ {name} accessible ({content_length} chars)")
            else:
                print(f"⚠️ {name} returned status: {response.status_code}")
                all_good = False
        except Exception as e:
            print(f"❌ Error testing {name}: {e}")
            all_good = False
    
    if all_good:
        print("\n🎉 ALL CONNECTIVITY TESTS PASSED!")
        print("\n🎯 Ready for next steps:")
        print("1. ✅ Chromium closed (manual)")
        print("2. ✅ Server running and accessible")
        print("3. ✅ All Office mocks responding")
        print("4. 🔄 Ready to test InteractiveUXAgent")
        
        print("\n🚀 To run the agent test:")
        print("   python simple_test.py")
        print("\n🔬 To run comprehensive tests:")
        print("   python tests/verify_word_mock.py")
        print("   python tests/verify_excel_mock.py")
        print("   python tests/verify_powerpoint_mock.py")
    else:
        print("\n❌ Some connectivity issues found")
        print("💡 Check server status and try again")
    
    return all_good

if __name__ == "__main__":
    test_connectivity()
