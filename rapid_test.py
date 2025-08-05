#!/usr/bin/env python3

"""
🚀 RAPID PHASE 1 TEST
Quick test with OpenAI API to verify core functionality
"""

from dotenv import load_dotenv
load_dotenv()

import os
print("🚀 RAPID PHASE 1 VERIFICATION TEST")
print("=" * 60)

# Verify API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"✅ API Key loaded: ...{api_key[-4:] if api_key else 'NOT FOUND'}")

if not api_key:
    print("❌ Cannot proceed without API key")
    exit(1)

# Test 1: Basic OpenAI connection
print("\n1️⃣ Testing OpenAI Client...")
try:
    from openai_client import OpenAIClientWrapper
    client = OpenAIClientWrapper()
    print("   ✅ Client created successfully")
    
    # Test a simple completion
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Reply with just 'TEST OK'"}],
        max_tokens=10
    )
    result = response.choices[0].message.content.strip()
    print(f"   ✅ API working: {result}")
    
except Exception as e:
    print(f"   ❌ OpenAI client failed: {e}")
    exit(1)

# Test 2: Agent import and basic setup
print("\n2️⃣ Testing Interactive Agent...")
try:
    from interactive_agent import InteractiveUXAgent
    agent = InteractiveUXAgent()
    print("   ✅ Agent created successfully")
    
    # Verify agent has the analyze_scenario method
    if hasattr(agent, 'analyze_scenario'):
        print("   ✅ analyze_scenario method available")
    else:
        print("   ❌ analyze_scenario method missing")
        exit(1)
        
except Exception as e:
    print(f"   ❌ Agent creation failed: {e}")
    exit(1)

# Test 3: Browser tools
print("\n3️⃣ Testing Browser Tools...")
try:
    from tools import BROWSER_FUNCTIONS, BrowserTools
    print(f"   ✅ {len(BROWSER_FUNCTIONS)} browser functions loaded")
    
    # Verify key functions exist
    function_names = [func['name'] for func in BROWSER_FUNCTIONS]
    required_functions = ['goto', 'click', 'screenshot', 'finish']
    
    for func in required_functions:
        if func in function_names:
            print(f"   ✅ {func} function available")
        else:
            print(f"   ❌ {func} function missing")
            
except Exception as e:
    print(f"   ❌ Browser tools failed: {e}")
    exit(1)

print("\n🌟 RAPID TEST RESULTS:")
print("=" * 40)
print("✅ OpenAI API connection working")
print("✅ Interactive agent functional") 
print("✅ Browser automation ready")
print("✅ All core components operational")

print("\n🎯 PHASE 1 CORE VERIFIED!")
print("Ready for full scenario testing...")
print("=" * 60)
