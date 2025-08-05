#!/usr/bin/env python3
"""
🔬 VS Code Runner - Execute Steps 2 & 3
Simple connectivity and agent test for VS Code execution
"""

import requests
import json

def test_connectivity():
    """Step 2: Test server and mocks"""
    print("🔍 STEP 2: CONNECTIVITY TEST")
    print("=" * 30)
    
    try:
        # Health check
        response = requests.get("http://localhost:8000/health", timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Server healthy!")
            print(f"📊 Mocks: {data.get('mocks_available', [])}")
            
            # Test mocks
            for mock in ['word.html', 'excel.html', 'powerpoint.html']:
                url = f"http://localhost:8000/mocks/{mock}"
                mock_resp = requests.get(url, timeout=3)
                if mock_resp.status_code == 200:
                    print(f"✅ {mock}: OK ({len(mock_resp.text)} chars)")
                else:
                    print(f"❌ {mock}: Failed")
                    return False
            
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connectivity failed: {e}")
        return False

def test_agent():
    """Step 3: Test agent basics"""
    print("\n🤖 STEP 3: AGENT TEST")
    print("=" * 25)
    
    try:
        import sys
        sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')
        
        from interactive_agent import InteractiveAgent
        print("✅ Agent import: OK")
        
        agent = InteractiveAgent()
        print("✅ Agent init: OK")
        
        # Test batching
        suggestions = agent._suggest_batch_optimizations("click button and type text")
        print(f"✅ Batching: {suggestions}")
        
        # Test client
        stats = agent.client.get_usage_stats()
        print(f"✅ Client: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

# Run tests
print("🧪 RUNNING STEPS 2 & 3")
print("=" * 25)

connectivity_ok = test_connectivity()
agent_ok = test_agent()

print(f"\n📊 RESULTS")
print("=" * 15)
print(f"Step 2 (Connectivity): {'✅ PASS' if connectivity_ok else '❌ FAIL'}")
print(f"Step 3 (Agent): {'✅ PASS' if agent_ok else '❌ FAIL'}")

if connectivity_ok and agent_ok:
    print("\n🎉 ALL TESTS PASSED!")
    print("🚀 Ready for full browser automation")
else:
    print("\n⚠️ Issues detected - check output above")
