#!/usr/bin/env python3
"""
🧪 Direct Test - No Web Interface Required
Test the enhanced UX system directly without needing the Flask app.
"""

def test_direct_access():
    print("🧪 TESTING ENHANCED UX SYSTEM DIRECTLY")
    print("=" * 50)
    print("This test bypasses the web interface to test core functionality.\n")
    
    try:
        # Test 1: Import check
        print("1️⃣ Testing imports...")
        from interactive_agent import InteractiveAgent
        print("✅ InteractiveAgent imported successfully")
        
        # Test 2: Agent initialization
        print("\n2️⃣ Testing agent initialization...")
        agent = InteractiveAgent()
        print("✅ Agent initialized successfully")
        
        # Test 3: Batching suggestions
        print("\n3️⃣ Testing batching optimization...")
        test_scenarios = [
            "Search for products on an e-commerce site",
            "Fill out a registration form",
            "Navigate to the contact page and send a message"
        ]
        
        for scenario in test_scenarios:
            suggestions = agent._suggest_batch_optimizations(scenario)
            print(f"📝 Scenario: {scenario}")
            print(f"💡 Suggestions: {suggestions}")
            print()
        
        print("✅ All direct tests passed!")
        print("\n🎯 SOLUTION FOR WEB ACCESS:")
        print("The correct URL for the web interface is:")
        print("🌐 http://127.0.0.1:5006  (not port 5000)")
        print("🌐 http://localhost:5006")
        print("\nTo start the web interface:")
        print("📝 Run: python3 app.py")
        print("📝 Or: python3 start_app.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_direct_access()
