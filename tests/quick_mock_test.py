#!/usr/bin/env python3
"""
🚀 Quick Office Mock Test - Fast Verification
Quick test to verify agent can connect to mocks
"""

import requests
import sys

def quick_connectivity_test():
    """Quick test of mock connectivity without full agent."""
    
    print("🚀 QUICK OFFICE MOCK CONNECTIVITY TEST")
    print("=" * 50)
    
    mocks = [
        ("Word", "http://localhost:8000/mocks/word.html"),
        ("Excel", "http://localhost:8000/mocks/excel.html"),
        ("PowerPoint", "http://localhost:8000/mocks/powerpoint.html")
    ]
    
    results = {}
    
    for mock_name, url in mocks:
        print(f"\\n🔍 Testing {mock_name} mock...")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {mock_name} mock accessible")
                
                # Check for expected content
                content = response.text.lower()
                
                # Mock-specific checks
                if mock_name == "Word":
                    expected = ["editor", "new-doc", "word"]
                elif mock_name == "Excel":
                    expected = ["grid", "cell", "formula", "excel"]
                elif mock_name == "PowerPoint":
                    expected = ["slide", "presentation", "powerpoint"]
                
                found = sum(1 for item in expected if item in content)
                if found >= len(expected) // 2:  # At least half the elements
                    print(f"   ✅ {mock_name} content validated ({found}/{len(expected)} elements)")
                    results[mock_name] = True
                else:
                    print(f"   ⚠️  {mock_name} content incomplete ({found}/{len(expected)} elements)")
                    results[mock_name] = False
                    
            else:
                print(f"   ❌ {mock_name} mock failed (status {response.status_code})")
                results[mock_name] = False
                
        except Exception as e:
            print(f"   ❌ {mock_name} mock error: {e}")
            results[mock_name] = False
    
    # Summary
    print("\\n📊 CONNECTIVITY TEST RESULTS:")
    print("=" * 35)
    
    passed = sum(results.values())
    total = len(results)
    
    for mock_name, success in results.items():
        icon = "✅" if success else "❌"
        print(f"{icon} {mock_name} Mock")
    
    print(f"\\n🎯 Result: {passed}/{total} mocks accessible")
    
    if passed == total:
        print("🌟 ALL MOCKS READY FOR AGENT TESTING!")
        return True
    else:
        print("🔧 Some mocks need attention")
        return False

def test_agent_import():
    """Test if InteractiveUXAgent can be imported."""
    print("\\n🤖 TESTING AGENT IMPORT...")
    try:
        from interactive_agent import InteractiveUXAgent
        print("   ✅ InteractiveUXAgent imported successfully")
        print("   🚀 Agent ready for mock testing")
        return True
    except Exception as e:
        print(f"   ❌ Agent import failed: {e}")
        return False

if __name__ == "__main__":
    print("🌐 Quick verification of Office mocks setup")
    print("⚡ Fast connectivity and content validation")
    
    connectivity_ok = quick_connectivity_test()
    agent_ok = test_agent_import()
    
    if connectivity_ok and agent_ok:
        print("\\n🎉 QUICK TEST: ✅ ALL SYSTEMS GO!")
        print("🚀 Ready for full end-to-end testing!")
        print("\\n📋 Next steps:")
        print("   1. Run: python tests/verify_word_mock.py")
        print("   2. Run: python tests/verify_excel_mock.py") 
        print("   3. Run: python tests/verify_powerpoint_mock.py")
        print("   4. Run: python yaml_runner.py")
    else:
        print("\\n🛠️  QUICK TEST: Issues detected")
        if not connectivity_ok:
            print("   🔧 Fix mock server connectivity")
        if not agent_ok:
            print("   🔧 Fix InteractiveUXAgent setup")
        sys.exit(1)
