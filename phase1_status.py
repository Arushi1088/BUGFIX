#!/usr/bin/env python3

"""
🔍 Quick Phase 1 Status Check
Verify all components are working without running full scenarios
"""

import sys
import os

def check_phase1_status():
    """Quick status check for Phase 1 components."""
    
    print("🔍 PHASE 1 STATUS CHECK")
    print("=" * 40)
    
    checks_passed = 0
    total_checks = 7
    
    # Check 1: Import InteractiveUXAgent
    try:
        from interactive_agent import InteractiveUXAgent
        print("✅ 1. InteractiveUXAgent import")
        checks_passed += 1
    except Exception as e:
        print(f"❌ 1. InteractiveUXAgent import failed: {e}")
    
    # Check 2: Import OpenAI client wrapper
    try:
        from openai_client import OpenAIClientWrapper
        print("✅ 2. OpenAI client wrapper import")
        checks_passed += 1
    except Exception as e:
        print(f"❌ 2. OpenAI client wrapper failed: {e}")
    
    # Check 3: Import browser tools
    try:
        from tools import BROWSER_FUNCTIONS, BrowserTools
        print(f"✅ 3. Browser tools ({len(BROWSER_FUNCTIONS)} functions)")
        checks_passed += 1
    except Exception as e:
        print(f"❌ 3. Browser tools failed: {e}")
    
    # Check 4: Create agent instance
    try:
        agent = InteractiveUXAgent()
        print("✅ 4. Agent instantiation")
        checks_passed += 1
    except Exception as e:
        print(f"❌ 4. Agent instantiation failed: {e}")
    
    # Check 5: Check agent methods
    try:
        if hasattr(agent, 'analyze_scenario'):
            print("✅ 5. analyze_scenario method available")
            checks_passed += 1
        else:
            print("❌ 5. analyze_scenario method missing")
    except:
        print("❌ 5. Could not check agent methods")
    
    # Check 6: Check client capabilities
    try:
        client = agent.client
        if hasattr(client, 'get_stats'):
            print("✅ 6. Client statistics available")
            checks_passed += 1
        else:
            print("❌ 6. Client statistics not available")
    except:
        print("❌ 6. Could not check client capabilities")
    
    # Check 7: Test HTML file creation
    try:
        test_file = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/test_page.html"
        if os.path.exists(test_file):
            print("✅ 7. Test HTML file exists")
        else:
            # Create simple test file
            with open(test_file, 'w') as f:
                f.write("<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Test Page</h1><button>Click Me</button></body></html>")
            print("✅ 7. Test HTML file created")
        checks_passed += 1
    except Exception as e:
        print(f"❌ 7. Test file creation failed: {e}")
    
    print(f"\\n📊 RESULTS: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🌟 ALL CHECKS PASSED - Phase 1 ready for testing!")
        return True
    elif checks_passed >= 5:
        print("⚠️  MOSTLY READY - Minor issues but core functionality available")
        return True
    else:
        print("❌ ISSUES FOUND - Need to fix core components")
        return False

if __name__ == "__main__":
    success = check_phase1_status()
    
    if success:
        print("\\n🚀 NEXT STEPS:")
        print("1. Run: python step1_unit_test.py (if you have OpenAI API key)")
        print("2. Start Flask: python app.py")
        print("3. Run: python step2_http_test.py")
        print("4. Run: python live_test.py (includes smoke check)")
        print("\\n✨ Then proceed to Phase 2!")
    else:
        print("\\n🔧 FIX ISSUES FIRST before proceeding")
    
    sys.exit(0 if success else 1)
