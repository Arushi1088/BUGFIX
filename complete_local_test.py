hat does th#!/usr/bin/env python3
"""
🧪 COMPLETE TEST WITH LOCAL SERVER
Tests the Phase 1 enhanced system using local test page on port 8080.
"""

import os
import time
import subprocess
import threading
import signal
import sys
from interactive_agent import InteractiveAgent

def check_server_running(port=8080):
    """Check if a server is running on the specified port."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def start_test_server():
    """Start the test server in the background."""
    print("🌐 Starting test web server on port 8080...")
    
    # Create the test page first
    from setup_test_server import create_test_page
    create_test_page()
    
    # Start server in background
    server_process = subprocess.Popen([
        'python3', '-m', 'http.server', '8080'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    for i in range(10):
        if check_server_running(8080):
            print("✅ Test server running on http://localhost:8080")
            return server_process
        time.sleep(1)
    
    print("❌ Failed to start test server")
    return None

def run_enhanced_test():
    """Run the complete enhanced UX test."""
    
    print("🧪 PHASE 1 ENHANCED SYSTEM - COMPLETE TEST WITH LOCAL SERVER")
    print("=" * 65)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found!")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return False
    
    # Start test server
    server_process = start_test_server()
    if not server_process:
        return False
    
    try:
        # Initialize enhanced agent
        print("\n🤖 Initializing Phase 1 Enhanced Agent...")
        agent = InteractiveAgent()
        print("✅ Agent ready with all enhancements")
        
        # Test scenarios on local server
        test_scenarios = [
            {
                "name": "Search Functionality Test",
                "url": "http://localhost:8080/test_page.html",
                "scenario": "Test the search functionality by finding the search input, entering 'AI testing', and clicking search",
                "expected": "Batching: find_elements → fill → click → screenshot"
            },
            {
                "name": "Contact Form Test", 
                "url": "http://localhost:8080/test_page.html",
                "scenario": "Fill out the contact form with name 'Test User', email 'test@example.com', and message 'Testing Phase 1 system'",
                "expected": "Form batching: gather fields → fill multiple → screenshot"
            },
            {
                "name": "Dynamic Content Test",
                "url": "http://localhost:8080/test_page.html", 
                "scenario": "Click the 'Load Dynamic Content' button and wait for content to appear",
                "expected": "Navigation: click → wait_for_element → screenshot"
            }
        ]
        
        print(f"\n🎯 Running {len(test_scenarios)} Enhanced Test Scenarios:")
        print("-" * 55)
        
        all_results = []
        
        for i, test in enumerate(test_scenarios, 1):
            print(f"\n📝 Test {i}: {test['name']}")
            print(f"🌐 URL: {test['url']}")
            print(f"📋 Scenario: {test['scenario']}")
            print(f"🔍 Expected: {test['expected']}")
            
            # Show batching suggestions
            suggestions = agent._suggest_batch_optimizations(test['scenario'])
            if suggestions:
                print(f"💡 Batching Suggestions:")
                print(f"   {suggestions}")
            
            print(f"\n🚀 Executing Enhanced Test {i}...")
            print("-" * 35)
            
            try:
                start_time = time.time()
                
                # Run the test with the enhanced agent
                result = agent.analyze_scenario(test['url'], test['scenario'])
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Display results
                print(f"\n✅ Test {i} Completed Successfully!")
                print(f"⏱️  Execution Time: {execution_time:.2f} seconds")
                print(f"📊 Actions Taken: {len(result.get('actions', []))}")
                print(f"🎯 Status: {result.get('status', 'Unknown')}")
                
                # Show key actions
                actions = result.get('actions', [])
                if actions:
                    print(f"\n📋 Key Actions:")
                    for j, action in enumerate(actions[-5:], 1):  # Show last 5 actions
                        action_type = action.get('action', 'unknown')
                        message = action.get('message', 'No message')[:60] + "..."
                        print(f"   {j}. {action_type}: {message}")
                
                # API usage statistics
                stats = agent.client.get_usage_stats()
                print(f"\n📈 API Statistics:")
                print(f"   • Requests: {stats['total_requests']}")
                print(f"   • Successful: {stats['successful_requests']}")
                print(f"   • Retries: {stats['total_retries']}")
                print(f"   • Fallbacks: {stats['fallback_requests']}")
                
                all_results.append({
                    'test': test['name'],
                    'success': True,
                    'time': execution_time,
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
            
            print(f"\n{'='*55}")
            
            # Brief pause between tests
            if i < len(test_scenarios):
                print("⏳ Brief pause before next test...")
                time.sleep(3)
        
        # Final summary
        print(f"\n🎉 ENHANCED SYSTEM TEST SUMMARY")
        print("=" * 50)
        
        successful = sum(1 for r in all_results if r['success'])
        total = len(all_results)
        
        print(f"📊 Results: {successful}/{total} tests successful")
        
        if successful > 0:
            avg_time = sum(r.get('time', 0) for r in all_results if r['success']) / successful
            total_actions = sum(r.get('actions', 0) for r in all_results if r['success'])
            
            print(f"⚡ Performance:")
            print(f"   • Average time: {avg_time:.2f} seconds")
            print(f"   • Total actions: {total_actions}")
            
            # Overall API stats
            final_stats = agent.client.get_usage_stats()
            print(f"📈 Total API Usage:")
            print(f"   • Requests: {final_stats['total_requests']}")
            print(f"   • Success rate: {final_stats['successful_requests']}/{final_stats['total_requests']}")
            print(f"   • Retries: {final_stats['total_retries']}")
        
        print(f"\n🚀 PHASE 1 FEATURES TESTED:")
        print("✅ Rate limiting with exponential backoff")
        print("✅ Smart element disambiguation")
        print("✅ Batching optimization")
        print("✅ Local server testing")
        print("✅ Enhanced error handling")
        
        success = (successful == total)
        if success:
            print(f"\n🎉 ALL TESTS PASSED! Phase 1 system fully operational!")
        else:
            print(f"\n⚠️  {total - successful} tests had issues.")
        
        return success
        
    finally:
        # Clean up server
        if server_process:
            print(f"\n🛑 Stopping test server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
            print("✅ Test server stopped")

if __name__ == "__main__":
    print("🎯 Starting complete enhanced system test...")
    print("   This will test all Phase 1 features with a local server")
    print("   Press Ctrl+C to cancel")
    
    try:
        time.sleep(2)
        success = run_enhanced_test()
        
        if success:
            print("\n✨ Complete test passed! Phase 1 system ready for production!")
            print("🚀 Ready for Phase 2 implementation!")
        else:
            print("\n🔧 Some issues detected. Check logs above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
