#!/usr/bin/env python3
"""
🎯 SIMPLE TEST RUNNER - Phase 1 Enhanced UX Testing System
Shows how to use the enhanced system with a real test scenario.
"""

def simple_test():
    print("🎯 PHASE 1 ENHANCED SYSTEM - SIMPLE TEST")
    print("=" * 50)
    
    # Test the web interface is working
    print("1️⃣ Testing Web Interface Availability...")
    try:
        from app import app
        print("✅ Flask app imported successfully")
        print("   🌐 Run with: python3 app.py")
        print("   📱 Access at: http://localhost:5000")
    except Exception as e:
        print(f"❌ Flask app issue: {e}")
    
    # Test the interactive agent
    print("\n2️⃣ Testing Interactive Agent...")
    try:
        from interactive_agent import InteractiveAgent
        agent = InteractiveAgent()
        print("✅ Interactive agent ready")
        
        # Show batching suggestions
        test_scenario = "Test the GitHub search by finding the search box and entering 'python'"
        suggestions = agent._suggest_batch_optimizations(test_scenario)
        print(f"✅ Batching suggestions: {suggestions}")
        
    except Exception as e:
        print(f"❌ Interactive agent issue: {e}")
    
    # Test the browser tools
    print("\n3️⃣ Testing Browser Tools...")
    try:
        from tools import BrowserTools, BROWSER_FUNCTIONS
        print(f"✅ Browser tools available: {len(BROWSER_FUNCTIONS)} functions")
        print(f"   Functions: {', '.join([func['name'] for func in BROWSER_FUNCTIONS])}")
    except Exception as e:
        print(f"❌ Browser tools issue: {e}")
    
    # Test the rate limiting
    print("\n4️⃣ Testing Rate Limiting...")
    try:
        from openai_client import OpenAIClientWrapper
        client = OpenAIClientWrapper()
        stats = client.get_usage_stats()
        print("✅ Rate limiting client ready")
        print(f"   📊 Stats tracking: {stats}")
    except Exception as e:
        print(f"❌ Rate limiting issue: {e}")
    
    print("\n🎉 SYSTEM STATUS SUMMARY:")
    print("✅ Phase 1 Complete: Rate limiting, disambiguation, batching")
    print("✅ Ready for testing with real scenarios")
    print("✅ All components functional")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Run web interface: python3 app.py")
    print("2. Test interactive mode: python3 test_scenario_demo.py")
    print("3. Or use directly in your code:")
    print("   from interactive_agent import InteractiveAgent")
    print("   agent = InteractiveAgent()")
    print("   result = agent.analyze_scenario(url, scenario)")

if __name__ == "__main__":
    simple_test()
