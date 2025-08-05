#!/usr/bin/env python3
"""
🔍 Integration Test Runner
Run just the integration navigation test
"""

import sys
import os
sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

from yaml_runner import YAMLTestRunner
from dotenv import load_dotenv

def run_integration_test():
    """Run only the integration navigation test."""
    print("🔍 INTEGRATION TEST RUNNER")
    print("=" * 30)
    
    # Load environment
    try:
        load_dotenv()
        print("✅ Environment loaded")
    except:
        print("⚠️ .env loading skipped")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found!")
        return False
    
    try:
        # Initialize runner
        runner = YAMLTestRunner()
        
        # Load schema
        if not runner.load_schema():
            print("❌ Failed to load YAML schema")
            return False
        
        print("✅ YAML schema loaded")
        
        # Check if integration tests exist
        if 'integration' not in runner.test_data:
            print("❌ No integration tests found in schema")
            return False
        
        integration_tests = runner.test_data['integration']
        print(f"📋 Found {len(integration_tests)} integration test(s)")
        
        # Find the navigation test
        nav_test = None
        for test in integration_tests:
            if 'Navigate between all Office apps' in test.get('scenario', ''):
                nav_test = test
                break
        
        if not nav_test:
            print("❌ Integration navigation test not found")
            return False
        
        print(f"🎯 Found test: {nav_test['scenario']}")
        print(f"📄 Description: {nav_test.get('description', 'N/A')}")
        
        # Run the test
        print("\n🚀 Running integration navigation test...")
        
        # Create a test suite for integration
        suite_results = runner.run_app_tests('integration', integration_tests)
        
        # Show results
        print(f"\n📊 INTEGRATION TEST RESULTS:")
        print(f"✅ Passed: {suite_results.passed}")
        print(f"❌ Failed: {suite_results.failed}")
        print(f"💥 Errors: {suite_results.errors}")
        print(f"⏱️  Duration: {suite_results.total_duration_ms}ms")
        
        if suite_results.results:
            result = suite_results.results[0]  # First (and likely only) result
            print(f"\n🔍 Test Details:")
            print(f"   Status: {result.status}")
            print(f"   Steps executed: {result.steps_executed}")
            print(f"   Expectations met: {result.expectations_met}/{result.expectations_total}")
            
            if result.errors:
                print(f"   Errors:")
                for error in result.errors:
                    print(f"     • {error}")
            
            if result.warnings:
                print(f"   Warnings:")
                for warning in result.warnings:
                    print(f"     • {warning}")
        
        success = suite_results.failed == 0 and suite_results.errors == 0
        
        if success:
            print(f"\n🎉 Integration test PASSED!")
        else:
            print(f"\n❌ Integration test FAILED")
        
        return success
        
    except Exception as e:
        print(f"❌ Error running integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Starting Integration Navigation Test...")
    
    try:
        success = run_integration_test()
        
        if success:
            print("\n✨ Integration test completed successfully!")
        else:
            print("\n🔧 Integration test needs attention")
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
