#!/usr/bin/env python3
"""
🧪 Quick Integration Mock Test
Simple test to verify integration.html works
"""

import requests
import sys

def test_integration_mock():
    """Quick test of integration mock."""
    print("🧪 QUICK INTEGRATION MOCK TEST")
    print("=" * 35)
    
    try:
        # Test integration mock
        print("🌐 Testing integration mock...")
        url = "http://localhost:8000/mocks/integration.html"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            content = response.text
            print(f"✅ Integration mock loaded ({len(content)} chars)")
            
            # Check for key elements
            checks = [
                ('data-testid="integration-title"', "Integration title"),
                ('data-testid="nav-word"', "Word navigation link"),
                ('data-testid="nav-excel"', "Excel navigation link"),
                ('data-testid="nav-powerpoint"', "PowerPoint navigation link"),
                ('Office Integration Hub', "Page title")
            ]
            
            all_good = True
            for check, desc in checks:
                if check in content:
                    print(f"✅ Found: {desc}")
                else:
                    print(f"❌ Missing: {desc}")
                    all_good = False
            
            if all_good:
                print("\n🎉 Integration mock is ready!")
                return True
            else:
                print("\n⚠️ Some elements missing")
                return False
                
        else:
            print(f"❌ Integration mock failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on localhost:8000")
        print("💡 Make sure server is running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_navigation_links():
    """Test that navigation targets exist."""
    print("\n🔗 Testing navigation targets...")
    
    targets = [
        ("Word", "http://localhost:8000/mocks/word.html"),
        ("Excel", "http://localhost:8000/mocks/excel.html"),
        ("PowerPoint", "http://localhost:8000/mocks/powerpoint.html")
    ]
    
    all_good = True
    for name, url in targets:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {name} mock accessible")
            else:
                print(f"❌ {name} mock failed: HTTP {response.status_code}")
                all_good = False
        except Exception as e:
            print(f"❌ {name} mock error: {e}")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🎯 Testing Integration Mock...")
    
    # Test integration mock
    integration_ok = test_integration_mock()
    
    # Test navigation targets
    nav_ok = test_navigation_links()
    
    print(f"\n📊 RESULTS:")
    print(f"Integration Mock: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    print(f"Navigation Links: {'✅ PASS' if nav_ok else '❌ FAIL'}")
    
    if integration_ok and nav_ok:
        print("\n🎉 Integration ready for testing!")
        print("🚀 Next: Run full YAML test with python yaml_runner.py")
    else:
        print("\n🔧 Fix issues above before proceeding")
    
    sys.exit(0 if integration_ok and nav_ok else 1)
