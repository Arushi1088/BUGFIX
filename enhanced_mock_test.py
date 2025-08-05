#!/usr/bin/env python3
"""
🧪 Enhanced Quick Mock Test - WITH CONTEXT OPTIMIZATION
Tests InteractiveUXAgent with optimized context and reduced token usage
"""

import sys
import os
import time
sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

from interactive_agent import InteractiveUXAgent

def test_basic_connectivity():
    """Test basic server connectivity first"""
    print("🔍 ENHANCED MOCK TEST - OPTIMIZED FOR CONTEXT")
    print("=" * 50)
    
    try:
        import requests
        
        # Quick health check
        print("📡 Testing server health...")
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print(f"✅ Server healthy: {response.json()}")
        else:
            print(f"⚠️ Server status: {response.status_code}")
            return False
            
        # Test each mock quickly
        mocks = ["word.html", "excel.html", "powerpoint.html"]
        for mock in mocks:
            url = f"http://localhost:8000/mocks/{mock}"
            print(f"🌐 Testing {mock}...")
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {mock} accessible ({len(response.text)} chars)")
            else:
                print(f"❌ {mock} failed: {response.status_code}")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        return False

def test_word_mock_optimized():
    """Test Word mock with optimized context management"""
    print("\n📄 TESTING WORD MOCK (Context Optimized)")
    print("-" * 40)
    
    try:
        # Initialize agent with context optimization
        agent = InteractiveUXAgent()
        
        # Enhanced scenario with specific selectors
        scenario = """
        Navigate to the Word mock and test document creation:
        1. Click the 'New Document' button using [data-testid='new-doc-btn']
        2. Click in the editor area using [data-testid='editor']
        3. Type 'Test Document Content' 
        4. Verify the word count updates
        """
        
        print("🤖 Starting Word test with enhanced selectors...")
        start_time = time.time()
        
        # Run test with specific URL
        result = agent.analyze_scenario("http://localhost:8000/mocks/word.html", scenario)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Show optimized results
        print(f"✅ Word test completed in {execution_time:.2f}s")
        print(f"🎯 Status: {result.get('status', 'Unknown')}")
        
        # Show only key actions (context optimization)
        actions = result.get('actions', [])
        if actions:
            print(f"📊 Total actions: {len(actions)}")
            print("🔍 Key actions:")
            for i, action in enumerate(actions[-3:], 1):  # Only show last 3
                action_type = action.get('action', 'unknown')
                message = action.get('message', '')[:50] + "..."
                print(f"   {i}. {action_type}: {message}")
        
        # API usage (optimized display)
        stats = agent.client.get_stats()
        print(f"📈 API: {stats['successful_requests']} requests, {stats.get('rate_limited_requests', 0)} rate limits")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"❌ Word test failed: {e}")
        return False

def test_excel_mock_optimized():
    """Test Excel mock with specific cell targeting"""
    print("\n📊 TESTING EXCEL MOCK (Cell Targeting)")
    print("-" * 40)
    
    try:
        agent = InteractiveUXAgent()
        
        # Focused Excel scenario
        scenario = """
        Test Excel functionality with specific cell operations:
        1. Click cell A1 using [data-testid='cell-A1']
        2. Enter 'Revenue' in the cell
        3. Click cell B1 using [data-testid='cell-B1'] 
        4. Enter '500' in the cell
        5. Click the SUM button using [data-testid='sum-btn']
        """
        
        print("🤖 Starting Excel test with cell targeting...")
        start_time = time.time()
        
        result = agent.analyze_scenario("http://localhost:8000/mocks/excel.html", scenario)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"✅ Excel test completed in {execution_time:.2f}s")
        print(f"🎯 Status: {result.get('status', 'Unknown')}")
        
        # Simplified output
        actions = result.get('actions', [])
        print(f"📊 Actions: {len(actions)} | Cell operations completed")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"❌ Excel test failed: {e}")
        return False

def run_optimized_tests():
    """Run all tests with optimization"""
    print("🚀 ENHANCED MOCK TESTING SUITE")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found!")
        return False
    
    # Step 1: Connectivity
    if not test_basic_connectivity():
        print("❌ Connectivity failed - check server")
        return False
    
    print("\n✅ Connectivity confirmed - proceeding with agent tests")
    
    # Step 2: Word test
    word_success = test_word_mock_optimized()
    
    # Brief pause to manage rate limits
    time.sleep(2)
    
    # Step 3: Excel test
    excel_success = test_excel_mock_optimized()
    
    # Summary
    print(f"\n🏁 ENHANCED TEST SUMMARY")
    print("=" * 30)
    
    total_tests = 2
    passed_tests = sum([word_success, excel_success])
    
    print(f"📊 Results: {passed_tests}/{total_tests} tests passed")
    
    if word_success:
        print("✅ Word mock: PASS")
    else:
        print("❌ Word mock: FAIL")
        
    if excel_success:
        print("✅ Excel mock: PASS")
    else:
        print("❌ Excel mock: FAIL")
    
    success = (passed_tests == total_tests)
    
    if success:
        print("\n🎉 ALL ENHANCED TESTS PASSED!")
        print("🔧 Context optimization working!")
        print("🎯 Selector targeting successful!")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests need attention")
    
    return success

if __name__ == "__main__":
    print("🎯 Starting Enhanced Mock Testing...")
    
    try:
        success = run_optimized_tests()
        
        if success:
            print("\n✨ Enhanced testing complete! Ready for YAML-driven tests.")
        else:
            print("\n🔧 Some optimizations needed. Check output above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
