#!/usr/bin/env python3
"""
🔧 MANUAL TEST SETUP
Step-by-step setup for testing the Phase 1 enhanced system.
"""

import os
import subprocess
import time

def setup_manual_test():
    print("🔧 MANUAL TEST SETUP - Phase 1 Enhanced System")
    print("=" * 55)
    
    print("\n📋 STEP-BY-STEP SETUP:")
    print("-" * 30)
    
    print("\n1️⃣ FIRST: Start the test web server")
    print("   📝 Run in Terminal 1:")
    print("      cd '/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer'")
    print("      python3 setup_test_server.py")
    print("   ✅ This will start server on http://localhost:8080")
    
    print("\n2️⃣ THEN: Set your OpenAI API key")
    print("   📝 Run in Terminal 2:")
    print("      export OPENAI_API_KEY='your-key-here'")
    
    print("\n3️⃣ FINALLY: Run the enhanced test")
    print("   📝 Choose one:")
    print("      Option A: python3 complete_local_test.py  # Full test")
    print("      Option B: python3 quick_test.py          # Quick check")
    print("      Option C: Manual Python test (see below)")
    
    print("\n🐍 OPTION C: MANUAL PYTHON TEST")
    print("-" * 35)
    print("   📝 Run this Python code:")
    print("""
from interactive_agent import InteractiveAgent

# Initialize the enhanced agent
agent = InteractiveAgent()

# Test with local server (make sure it's running on port 8080)
result = agent.analyze_scenario(
    "http://localhost:8080/test_page.html",
    "Test the search functionality by finding the search input and entering 'AI testing'"
)

print(f"✅ Test completed!")
print(f"📊 Actions taken: {len(result.get('actions', []))}")
print(f"🎯 Status: {result.get('status')}")

# Check the enhanced features
stats = agent.client.get_usage_stats()
print(f"📈 API Usage: {stats}")
    """)
    
    print("\n🎯 WHAT TO EXPECT:")
    print("-" * 20)
    print("✅ Batching suggestions displayed before test")
    print("✅ Multiple actions processed per turn")
    print("✅ Single screenshot after action sequences")
    print("✅ Smart element disambiguation if needed")
    print("✅ Rate limiting statistics at the end")
    
    print("\n🛠️ TROUBLESHOOTING:")
    print("-" * 20)
    print("❌ If port 8080 is busy:")
    print("   📝 lsof -ti:8080 | xargs kill")
    print("❌ If imports fail:")
    print("   📝 Check you're in the right directory")
    print("❌ If API key issues:")
    print("   📝 echo $OPENAI_API_KEY  # should show your key")

def quick_server_check():
    """Quick check if server setup is possible."""
    print("\n🔍 QUICK ENVIRONMENT CHECK:")
    print("-" * 30)
    
    # Check if we're in the right directory
    if os.path.exists('interactive_agent.py'):
        print("✅ In correct directory")
    else:
        print("❌ Wrong directory - navigate to ux-analyzer folder")
        return False
    
    # Check if test server setup exists
    if os.path.exists('setup_test_server.py'):
        print("✅ Test server setup available")
    else:
        print("❌ Test server setup missing")
        return False
    
    # Check OpenAI key
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key is set")
    else:
        print("⚠️  OpenAI API key not set (needed for full test)")
    
    # Check if port 8080 is free
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        if result == 0:
            print("⚠️  Port 8080 is in use")
        else:
            print("✅ Port 8080 is available")
    except:
        print("✅ Port 8080 appears available")
    
    return True

if __name__ == "__main__":
    setup_manual_test()
    
    if quick_server_check():
        print("\n🚀 READY TO TEST!")
        print("Follow the steps above to test the Phase 1 enhanced system.")
    else:
        print("\n🔧 Fix the issues above before testing.")
        
    print("\n💡 For automatic test, run: python3 complete_local_test.py")
