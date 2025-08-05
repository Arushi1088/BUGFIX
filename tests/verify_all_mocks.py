#!/usr/bin/env python3
"""
🧪 All Office Mocks Verification - Complete End-to-End Test Suite
Run all Office mock verifications in sequence
"""

import sys
import os
import time
import requests

def check_server():
    """Check if server is running before tests."""
    print("🔍 CHECKING SERVER STATUS")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Server is not accessible")
        print("💡 Please start server with: python server.py")
        return False

def run_mock_test(test_file, mock_name):
    """Run a specific mock test."""
    print(f"\\n🧪 TESTING {mock_name.upper()} MOCK")
    print("=" * 50)
    
    try:
        # Import and run the test
        test_module = __import__(f"tests.{test_file}", fromlist=[test_file])
        
        if hasattr(test_module, f'test_{test_file.split("_")[1]}_mock'):
            test_function = getattr(test_module, f'test_{test_file.split("_")[1]}_mock')
            result = test_function()
            return result
        else:
            print(f"❌ Test function not found in {test_file}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to run {mock_name} test: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_verifications():
    """Run all Office mock verifications."""
    
    print("🎯 OFFICE MOCKS END-TO-END VERIFICATION SUITE")
    print("=" * 60)
    print("🤖 Testing InteractiveUXAgent with all Office mocks")
    print("🌐 Server: http://localhost:8000")
    
    # Check server first
    if not check_server():
        print("\\n💥 VERIFICATION FAILED: Server not accessible")
        return False
    
    # Test results tracking
    results = {}
    test_configs = [
        ("verify_word_mock", "Word"),
        ("verify_excel_mock", "Excel"), 
        ("verify_powerpoint_mock", "PowerPoint")
    ]
    
    print("\\n🚀 STARTING MOCK VERIFICATIONS...")
    
    for test_file, mock_name in test_configs:
        print(f"\\n{'='*20} {mock_name} Test {'='*20}")
        
        try:
            # Run individual test script
            python_cmd = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/.venv/bin/python"
            test_path = f"tests/{test_file}.py"
            
            import subprocess
            result = subprocess.run(
                [python_cmd, test_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                print(f"✅ {mock_name} mock test: PASSED")
                results[mock_name] = True
                
                # Show some output
                if result.stdout:
                    lines = result.stdout.strip().split('\\n')
                    if len(lines) > 10:
                        print("📊 Test Output (last 5 lines):")
                        for line in lines[-5:]:
                            print(f"   {line}")
                    else:
                        print("📊 Test Output:")
                        for line in lines:
                            print(f"   {line}")
            else:
                print(f"❌ {mock_name} mock test: FAILED")
                results[mock_name] = False
                
                if result.stderr:
                    print("🚨 Error Output:")
                    print(result.stderr)
                    
        except subprocess.TimeoutExpired:
            print(f"⏰ {mock_name} mock test: TIMEOUT (5 minutes)")
            results[mock_name] = False
        except Exception as e:
            print(f"💥 {mock_name} mock test: EXCEPTION ({e})")
            results[mock_name] = False
    
    # Summary
    print("\\n📊 VERIFICATION RESULTS SUMMARY")
    print("=" * 40)
    
    passed_tests = 0
    total_tests = len(results)
    
    for mock_name, success in results.items():
        icon = "✅" if success else "❌"
        print(f"{icon} {mock_name} Mock: {'PASSED' if success else 'FAILED'}")
        if success:
            passed_tests += 1
    
    print(f"\\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🌟 ALL OFFICE MOCKS VERIFICATION: ✅ SUCCESS!")
        print("🚀 InteractiveUXAgent can drive all Office mocks!")
        return True
    elif passed_tests > 0:
        print("🟡 PARTIAL SUCCESS - Some mocks working")
        print("🔧 Check failed tests for issues")
        return False
    else:
        print("🔴 ALL TESTS FAILED")
        print("🛠️  Check agent setup and server configuration")
        return False

if __name__ == "__main__":
    print("🌟 Starting comprehensive Office mocks verification...")
    print("⏱️  This may take several minutes due to agent initialization")
    
    success = run_all_verifications()
    
    if success:
        print("\\n🎉 Office mocks verification completed successfully!")
        print("🚀 Ready for YAML-driven testing and advanced features!")
    else:
        print("\\n🛠️  Some verifications failed - check individual test outputs")
        sys.exit(1)
