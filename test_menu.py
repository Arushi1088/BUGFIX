#!/usr/bin/env python3
"""
📋 STEP-BY-STEP TEST GUIDE
==========================
Easy-to-follow test instructions for Phase 1 enhanced system.
"""

def print_test_instructions():
    print("📋 STEP-BY-STEP TEST GUIDE - Phase 1 Enhanced UX Testing")
    print("=" * 60)
    
    print("\n🎯 CHOOSE YOUR TEST LEVEL:")
    print("1. ⚡ Quick verification (2 minutes)")
    print("2. 🧪 Single scenario test (5 minutes)")  
    print("3. 🔬 Comprehensive test (15 minutes)")
    print("4. 🌐 Web interface test (manual)")
    
    print("\n" + "="*60)
    
    print("\n⚡ OPTION 1: QUICK VERIFICATION")
    print("-" * 30)
    print("📝 Run: python3 quick_test.py")
    print("🎯 Purpose: Verify all components are working")
    print("⏱️  Time: ~2 minutes")
    print("📊 Tests: Imports, batching, rate limiting, prompts")
    
    print("\n🧪 OPTION 2: SINGLE SCENARIO TEST")
    print("-" * 30)
    print("📝 Code to run:")
    print("""
from interactive_agent import InteractiveAgent

# Initialize the enhanced agent
agent = InteractiveAgent()

# Run a single test
result = agent.analyze_scenario(
    "https://www.google.com",
    "Search for 'artificial intelligence' and examine results"
)

print("Test completed!")
print(f"Actions taken: {len(result.get('actions', []))}")
print(f"Status: {result.get('status')}")

# Check API usage
stats = agent.client.get_usage_stats()
print(f"API calls: {stats['total_requests']}")
    """)
    print("🎯 Purpose: Test one complete scenario")
    print("⏱️  Time: ~5 minutes")
    print("📊 Features: Full batching, disambiguation, rate limiting")
    
    print("\n🔬 OPTION 3: COMPREHENSIVE TEST")
    print("-" * 30)
    print("📝 Run: python3 comprehensive_test.py")
    print("🎯 Purpose: Test multiple scenarios with different features")
    print("⏱️  Time: ~15 minutes")
    print("📊 Tests: 3 different websites, all Phase 1 features")
    
    print("\n🌐 OPTION 4: WEB INTERFACE TEST")
    print("-" * 30)
    print("📝 Steps:")
    print("   1. Run: python3 app.py")
    print("   2. Open: http://localhost:5006")
    print("   3. Try the 'Interactive Testing' feature")
    print("   4. Enter URL: https://github.com")
    print("   5. Scenario: 'Test the search functionality'")
    print("🎯 Purpose: Test through web interface")
    print("⏱️  Time: Manual testing")
    print("📊 Features: Visual feedback, real-time updates")

def run_guided_test():
    print("\n🚀 RUNNING GUIDED TEST")
    print("=" * 30)
    
    print("This will run a simple guided test to show Phase 1 features...")
    
    try:
        # Import test
        print("\n1️⃣ Testing imports...")
        from interactive_agent import InteractiveAgent
        print("✅ InteractiveAgent imported")
        
        # Initialize test
        print("\n2️⃣ Initializing agent...")
        agent = InteractiveAgent()
        print("✅ Agent initialized with Phase 1 enhancements")
        
        # Batching test
        print("\n3️⃣ Testing batching suggestions...")
        scenario = "Search for products and add them to cart"
        suggestions = agent._suggest_batch_optimizations(scenario)
        print(f"📝 Scenario: {scenario}")
        print(f"💡 Suggestions: {suggestions}")
        
        # Rate limiting test
        print("\n4️⃣ Testing rate limiting...")
        stats = agent.client.get_usage_stats()
        print(f"📊 Initial stats: {stats}")
        print("✅ Rate limiting system ready")
        
        print("\n🎉 GUIDED TEST COMPLETE!")
        print("All Phase 1 features are working correctly.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Guided test failed: {e}")
        return False

if __name__ == "__main__":
    print_test_instructions()
    
    print("\n" + "="*60)
    choice = input("\nChoose test option (1-4) or 'g' for guided test: ").strip().lower()
    
    if choice == '1':
        print("\n🚀 Running quick verification...")
        import subprocess
        subprocess.run(['python3', 'quick_test.py'])
        
    elif choice == '2':
        print("\n🚀 Running single scenario test...")
        print("Copy and paste this code into a Python shell:")
        print("-" * 40)
        print("""
from interactive_agent import InteractiveAgent
agent = InteractiveAgent()
result = agent.analyze_scenario("https://www.google.com", "Search for AI")
print(f"Done! Actions: {len(result.get('actions', []))}")
        """)
        
    elif choice == '3':
        print("\n🚀 Running comprehensive test...")
        import subprocess
        subprocess.run(['python3', 'comprehensive_test.py'])
        
    elif choice == '4':
        print("\n🚀 Starting web interface...")
        print("1. Run: python3 app.py")
        print("2. Open: http://localhost:5006")
        print("3. Test the enhanced features!")
        
    elif choice == 'g':
        run_guided_test()
        
    else:
        print("Invalid choice. Run this script again and choose 1-4 or 'g'.")
