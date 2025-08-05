#!/usr/bin/env python3
"""
🧪 Direct Word Mock Test
Simple direct test execution
"""

import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print("🎯 DIRECT WORD MOCK SMOKE TEST")
print("=" * 40)

# Test 1: Check imports
print("1️⃣ Testing imports...")
try:
    from interactive_agent import InteractiveUXAgent
    print("   ✅ InteractiveUXAgent imported")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check server connectivity  
print("\\n2️⃣ Testing server connectivity...")
try:
    import requests
    response = requests.get("http://localhost:8000/mocks/word.html", timeout=5)
    if response.status_code == 200:
        print("   ✅ Word mock accessible")
    else:
        print(f"   ❌ Word mock failed: {response.status_code}")
        print("   💡 Start server with: python server.py")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Server connection failed: {e}")
    print("   💡 Start server with: python server.py") 
    sys.exit(1)

# Test 3: Initialize agent
print("\\n3️⃣ Initializing InteractiveUXAgent...")
try:
    agent = InteractiveUXAgent()
    print("   ✅ Agent initialized successfully")
except Exception as e:
    print(f"   ❌ Agent initialization failed: {e}")
    sys.exit(1)

# Test 4: Run scenario
print("\\n4️⃣ Running Word mock scenario...")
try:
    result = agent.analyze_scenario(
        url="http://localhost:8000/mocks/word.html",
        scenario="Navigate to the Word mock and check if it loads properly"
    )
    
    print(f"   📊 Status: {result.get('status', 'unknown')}")
    
    actions = result.get('actions_taken', [])
    print(f"   🔧 Actions taken: {len(actions)}")
    
    for i, action in enumerate(actions[:3], 1):  # Show first 3 actions
        success = "✅" if action.get('success', False) else "❌"
        action_type = action.get('action', 'unknown')
        print(f"      {i}. {action_type} {success}")
    
    if result.get('status') == 'success':
        print("   🎉 Word mock test PASSED!")
    else:
        print("   ⚠️  Word mock test had issues")
        
except Exception as e:
    print(f"   ❌ Scenario execution failed: {e}")
    import traceback
    traceback.print_exc()

print("\\n🚀 Direct Word mock test completed!")
print("📝 Ready for Excel and PowerPoint tests!")
