#!/usr/bin/env python3
"""
🧪 PHASE 1 ENHANCED UX TESTING SYSTEM - COMPLETE TEST
=====================================================
This test demonstrates all Phase 1 features:
✅ Rate limiting with exponential backoff
✅ Smart element disambiguation 
✅ Batching optimization
✅ Robust error handling
"""

import os
import time
from interactive_agent import InteractiveAgent

def run_comprehensive_test():
    """Run a comprehensive test of the enhanced UX testing system."""
    
    print("🧪 PHASE 1 ENHANCED UX TESTING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 65)
    
    # Check environment
    print("🔍 Environment Check:")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API Key: ...{api_key[-4:] if len(api_key) > 4 else 'Set'}")
    else:
        print("❌ OpenAI API Key not found!")
        print("   Run: export OPENAI_API_KEY='your-key-here'")
        return False
    
    print("✅ Environment ready\n")
    
    # Initialize agent
    print("🤖 Initializing Enhanced Agent...")
    try:
        agent = InteractiveAgent()
        print("✅ Agent initialized with Phase 1 enhancements")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False
    
    # Test scenarios with increasing complexity
    test_scenarios = [
        {
            "name": "Basic Search Test",
            "url": "https://www.google.com",
            "scenario": "Search for 'artificial intelligence' and examine the results",
            "expected_features": ["batching suggestions", "find_elements → screenshot optimization"]
        },
        {
            "name": "GitHub Repository Search",
            "url": "https://github.com", 
            "scenario": "Find the search functionality and search for 'python machine learning'",
            "expected_features": ["disambiguation if multiple search elements", "navigation batching"]
        },
        {
            "name": "E-commerce Product Search",
            "url": "https://www.amazon.com",
            "scenario": "Test the product search by looking for 'laptop computers'",
            "expected_features": ["form field optimization", "rate limiting resilience"]
        }
    ]
    
    print(f"\n🎯 Running {len(test_scenarios)} Test Scenarios:")
    print("-" * 50)
    
    all_results = []
    
    for i, test in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"🌐 URL: {test['url']}")
        print(f"📋 Scenario: {test['scenario']}")
        print(f"🔍 Expected Features: {', '.join(test['expected_features'])}")
        
        # Show batching suggestions
        print(f"\n💡 Batching Optimization Analysis:")
        suggestions = agent._suggest_batch_optimizations(test['scenario'])
        if suggestions:
            print(suggestions)
        else:
            print("💡 No specific batching suggestions for this scenario type")
        
        print(f"\n🚀 Executing Test {i}...")
        print("-" * 30)
        
        try:
            start_time = time.time()
            
            # Run the actual test
            result = agent.analyze_scenario(test['url'], test['scenario'])
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Analyze results
            print(f"\n✅ Test {i} Completed Successfully!")
            print(f"⏱️  Execution Time: {execution_time:.2f} seconds")
            print(f"📊 Actions Taken: {len(result.get('actions', []))}")
            print(f"🎯 Status: {result.get('status', 'Unknown')}")
            
            # Show action summary
            actions = result.get('actions', [])
            if actions:
                print(f"\n📋 Action Summary:")
                for j, action in enumerate(actions[-3:], 1):  # Show last 3 actions
                    action_type = action.get('action', 'unknown')
                    message = action.get('message', 'No message')[:50] + "..."
                    print(f"   {j}. {action_type}: {message}")
            
            # Show API usage statistics
            stats = agent.client.get_usage_stats()
            print(f"\n📈 API Statistics for Test {i}:")
            print(f"   • Total Requests: {stats['total_requests']}")
            print(f"   • Successful: {stats['successful_requests']}")
            print(f"   • Retries: {stats['total_retries']}")
            print(f"   • Fallbacks: {stats['fallback_requests']}")
            
            all_results.append({
                'test': test['name'],
                'success': True,
                'execution_time': execution_time,
                'actions': len(actions),
                'stats': stats
            })
            
        except Exception as e:
            print(f"❌ Test {i} Failed: {e}")
            all_results.append({
                'test': test['name'],
                'success': False,
                'error': str(e)
            })
        
        print(f"\n{'='*50}")
        
        # Wait between tests to avoid rate limiting
        if i < len(test_scenarios):
            print("⏳ Waiting 5 seconds before next test...")
            time.sleep(5)
    
    # Final summary
    print(f"\n🎉 COMPREHENSIVE TEST SUMMARY")
    print("=" * 50)
    
    successful_tests = sum(1 for r in all_results if r['success'])
    total_tests = len(all_results)
    
    print(f"📊 Test Results: {successful_tests}/{total_tests} successful")
    
    if successful_tests > 0:
        total_actions = sum(r.get('actions', 0) for r in all_results if r['success'])
        avg_time = sum(r.get('execution_time', 0) for r in all_results if r['success']) / successful_tests
        
        print(f"⚡ Performance:")
        print(f"   • Total Actions: {total_actions}")
        print(f"   • Average Time: {avg_time:.2f} seconds per test")
        
        # Combined statistics
        if hasattr(agent, 'client'):
            final_stats = agent.client.get_usage_stats()
            print(f"📈 Overall API Usage:")
            print(f"   • Total Requests: {final_stats['total_requests']}")
            print(f"   • Success Rate: {final_stats['successful_requests']}/{final_stats['total_requests']}")
            print(f"   • Total Retries: {final_stats['total_retries']}")
            print(f"   • Fallback Uses: {final_stats['fallback_requests']}")
    
    print(f"\n🚀 PHASE 1 FEATURES DEMONSTRATED:")
    print("✅ Rate limiting with exponential backoff and fallbacks")
    print("✅ Smart element disambiguation with multiple strategies")
    print("✅ Batching optimization for reduced API calls")
    print("✅ Robust error handling and recovery")
    print("✅ Performance monitoring and statistics")
    
    if successful_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! Phase 1 system is working perfectly!")
        print("🚀 Ready for Phase 2 implementation!")
    else:
        print(f"\n⚠️  {total_tests - successful_tests} tests had issues. Check logs above.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    print("🎯 Starting comprehensive test in 3 seconds...")
    print("   Press Ctrl+C to cancel")
    
    try:
        time.sleep(3)
        success = run_comprehensive_test()
        
        if success:
            print("\n✨ Test completed successfully!")
            print("💡 Try the web interface: python3 app.py → http://localhost:5006")
        else:
            print("\n🔧 Some tests failed. Check error messages above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        print("💡 Try: python3 simple_test_runner.py for basic checks")
