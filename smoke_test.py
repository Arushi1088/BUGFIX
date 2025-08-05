#!/usr/bin/env python3
"""
🧪 Smoke Test for Interactive UX Agent
Tests the complete interactive loop with known UX issues.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()

from interactive_agent import InteractiveUXAgent

def run_smoke_tests():
    """Run comprehensive smoke tests for the interactive UX agent."""
    
    print("🧪 Starting Interactive UX Agent Smoke Tests")
    print("=" * 60)
    
    # Get the absolute path to our test HTML file
    test_file_path = project_root / "test_page.html"
    test_url = f"file://{test_file_path.absolute()}"
    
    print(f"🌐 Test URL: {test_url}")
    
    # Initialize the agent
    agent = InteractiveUXAgent()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Contact Button Test",
            "scenario": "Find and click the 'Contact Us' button to open the contact form",
            "expected_actions": ["goto", "screenshot", "click", "finish"],
            "should_complete": True
        },
        {
            "name": "Learn More Test", 
            "scenario": "Click the 'Learn More' button and verify the action",
            "expected_actions": ["goto", "click", "finish"],
            "should_complete": True
        },
        {
            "name": "Form Filling Test",
            "scenario": "Fill out and submit the main form on the page",
            "expected_actions": ["goto", "fill", "click", "finish"],
            "should_complete": True
        },
        {
            "name": "Navigation Test",
            "scenario": "Use the navigation menu to go to the Contact section",
            "expected_actions": ["goto", "click", "finish"],
            "should_complete": True
        },
        {
            "name": "UX Issues Detection",
            "scenario": "Analyze the page for UX and accessibility issues without performing specific tasks",
            "expected_actions": ["goto", "screenshot", "finish"],
            "should_complete": True
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_scenarios, 1):
        print(f"\\n🎯 Test {i}/{len(test_scenarios)}: {test['name']}")
        print(f"📝 Scenario: {test['scenario']}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            # Run the interactive analysis
            result = agent.analyze_scenario(test_url, test['scenario'])
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Analyze results
            success = result.get('status') == 'success'
            actions_taken = result.get('actions_taken', [])
            action_count = result.get('action_count', 0)
            
            print(f"\\n📊 Test Results:")
            print(f"   ✅ Status: {result.get('status', 'unknown')}")
            print(f"   🔢 Actions: {action_count}")
            print(f"   ⏱️  Duration: {duration:.2f}s")
            
            if actions_taken:
                print(f"   🎬 Actions taken:")
                for j, action in enumerate(actions_taken, 1):
                    action_name = action.get('action', 'unknown')
                    action_success = action.get('success', False)
                    status_icon = "✅" if action_success else "❌"
                    print(f"      {j}. {status_icon} {action_name}")
                    
            # Check if expected actions were performed
            actual_actions = [a.get('action') for a in actions_taken]
            missing_actions = []
            for expected in test['expected_actions']:
                if expected not in actual_actions:
                    missing_actions.append(expected)
            
            if missing_actions:
                print(f"   ⚠️  Missing expected actions: {missing_actions}")
            
            # Store result
            test_result = {
                'name': test['name'],
                'success': success,
                'duration': duration,
                'action_count': action_count,
                'actions_taken': actual_actions,
                'missing_actions': missing_actions,
                'raw_result': result
            }
            results.append(test_result)
            
            if success:
                print(f"   🎉 Test PASSED")
            else:
                print(f"   💥 Test FAILED: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   💥 Test CRASHED: {e}")
            results.append({
                'name': test['name'],
                'success': False,
                'error': str(e),
                'duration': time.time() - start_time
            })
    
    # Print summary
    print("\\n" + "=" * 60)
    print("📈 SMOKE TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    for result in results:
        status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
        duration = result.get('duration', 0)
        actions = result.get('action_count', 0)
        print(f"{status} | {result['name']:<25} | {duration:>6.1f}s | {actions:>2} actions")
    
    # Detailed analysis for failures
    failures = [r for r in results if not r.get('success', False)]
    if failures:
        print(f"\\n💥 FAILED TESTS ({len(failures)}):")
        for failure in failures:
            print(f"\\n❌ {failure['name']}:")
            if 'error' in failure:
                print(f"   Error: {failure['error']}")
            if 'missing_actions' in failure and failure['missing_actions']:
                print(f"   Missing actions: {failure['missing_actions']}")
    
    print(f"\\n🏁 Smoke tests completed!")
    return passed == total

if __name__ == "__main__":
    try:
        success = run_smoke_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
