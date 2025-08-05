#!/usr/bin/env python3
"""
🎉 COMPREHENSIVE SMOKE TEST RESULTS
Office Mocks End-to-End Verification Summary
"""

import requests
import time
import sys
import os

def test_server_connectivity():
    """Test if all mocks are accessible."""
    print("🌐 TESTING SERVER CONNECTIVITY")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    mocks = {
        "Home Page": "",
        "Word Mock": "/mocks/word.html",
        "Excel Mock": "/mocks/excel.html", 
        "PowerPoint Mock": "/mocks/powerpoint.html",
        "Health Check": "/health"
    }
    
    results = {}
    
    for name, endpoint in mocks.items():
        url = base_url + endpoint
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: ACCESSIBLE")
                results[name] = True
                
                # Check content for mocks
                if "mock" in endpoint.lower():
                    content = response.text.lower()
                    if any(word in content for word in ["microsoft", "office", "mock"]):
                        print(f"   📄 Content validated")
                    else:
                        print(f"   ⚠️  Content may be incomplete")
                        
            else:
                print(f"❌ {name}: FAILED ({response.status_code})")
                results[name] = False
                
        except Exception as e:
            print(f"❌ {name}: ERROR ({e})")
            results[name] = False
    
    return results

def test_agent_readiness():
    """Test if InteractiveUXAgent can be imported."""
    print("\\n🤖 TESTING AGENT READINESS")
    print("=" * 30)
    
    try:
        # Change to project directory
        os.chdir("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")
        
        # Test import
        from interactive_agent import InteractiveUXAgent
        print("✅ InteractiveUXAgent: IMPORTABLE")
        
        # Test basic initialization (without full setup to avoid timeout)
        print("✅ Agent module: LOADED")
        return True
        
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False

def test_yaml_system():
    """Test YAML system readiness."""
    print("\\n📋 TESTING YAML SYSTEM")
    print("=" * 25)
    
    try:
        import yaml
        print("✅ PyYAML: AVAILABLE")
        
        # Test schema loading
        with open("schemas/office_tests.yaml", 'r') as f:
            schema = yaml.safe_load(f)
        
        tests_count = len(schema.get('tests', []))
        print(f"✅ Test scenarios: {tests_count} LOADED")
        
        # Test runner import
        from yaml_runner import YAMLTestRunner
        print("✅ YAMLTestRunner: IMPORTABLE")
        
        return True
        
    except Exception as e:
        print(f"❌ YAML system error: {e}")
        return False

def run_comprehensive_assessment():
    """Run comprehensive smoke test assessment."""
    
    print("🎯 COMPREHENSIVE OFFICE MOCKS SMOKE TEST")
    print("=" * 50)
    print("📅 Test Date: 29 July 2025")
    print("🌐 Server: http://localhost:8000")
    print("🤖 Agent: InteractiveUXAgent")
    print("📋 System: YAML-driven testing")
    
    # Run tests
    connectivity_results = test_server_connectivity()
    agent_ready = test_agent_readiness()
    yaml_ready = test_yaml_system()
    
    # Calculate scores
    connectivity_score = sum(connectivity_results.values())
    connectivity_total = len(connectivity_results)
    
    # Summary
    print("\\n📊 SMOKE TEST RESULTS SUMMARY")
    print("=" * 40)
    
    print(f"🌐 Server Connectivity: {connectivity_score}/{connectivity_total}")
    for name, success in connectivity_results.items():
        icon = "✅" if success else "❌"
        print(f"   {icon} {name}")
    
    print(f"\\n🤖 Agent Readiness: {'✅ YES' if agent_ready else '❌ NO'}")
    print(f"📋 YAML System: {'✅ YES' if yaml_ready else '❌ NO'}")
    
    # Overall assessment
    all_connectivity = connectivity_score == connectivity_total
    all_systems = agent_ready and yaml_ready
    
    print("\\n🎯 OVERALL ASSESSMENT:")
    print("=" * 25)
    
    if all_connectivity and all_systems:
        print("🌟 COMPREHENSIVE SMOKE TEST: ✅ PASSED")
        print("🚀 ALL SYSTEMS OPERATIONAL!")
        print("\\n✅ Ready for:")
        print("   • InteractiveUXAgent automation")
        print("   • YAML-driven test scenarios") 
        print("   • End-to-end Office mock testing")
        print("   • Advanced UX analysis")
        return True
    elif all_connectivity:
        print("🟡 PARTIAL SUCCESS")
        print("🌐 Server and mocks working")
        print("🔧 Agent/YAML systems need attention")
        return False
    else:
        print("🔴 SMOKE TEST FAILED")
        print("🛠️  Multiple systems need fixing")
        return False

def show_next_steps():
    """Show available next steps."""
    print("\\n🚀 AVAILABLE NEXT STEPS:")
    print("=" * 30)
    print("1. 🧪 Manual Testing:")
    print("   • Test mocks in open browser tabs")
    print("   • Verify interactive functionality")
    print("\\n2. 🤖 Agent Testing:")
    print("   • python tests/verify_word_mock.py")
    print("   • python tests/verify_excel_mock.py")
    print("   • python tests/verify_powerpoint_mock.py")
    print("\\n3. 📋 YAML Testing:")
    print("   • python yaml_runner.py")
    print("\\n4. 🔄 Complete Suite:")
    print("   • python tests/verify_all_mocks.py")

if __name__ == "__main__":
    success = run_comprehensive_assessment()
    show_next_steps()
    
    if success:
        print("\\n🎉 SMOKE TEST COMPLETE!")
        print("🌟 Office mocks system fully operational!")
    else:
        print("\\n🛠️  Some components need attention")
        print("📋 Check individual test results above")
    
    sys.exit(0 if success else 1)
