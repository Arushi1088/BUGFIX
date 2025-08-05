#!/usr/bin/env python3
"""
🎯 PHASE 2 TEST LAUNCHER
Complete test suite execution
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_command(cmd, description, timeout=30):
    """Run a command with timeout."""
    print(f"\n🔄 {description}")
    print(f"💻 Command: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=str(project_root)
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"📝 Output:\n{result.stdout}")
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"⚠️ Error:\n{result.stderr}")
            if result.stdout.strip():
                print(f"📝 Output:\n{result.stdout}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {e}")
        return False

def check_server():
    """Check if server is running."""
    print("🌐 Checking server status...")
    return run_command("curl -s http://localhost:8000/health", "Server health check", 5)

def run_tests():
    """Run all Phase 2 tests."""
    print("🎯 PHASE 2 TEST EXECUTION")
    print("=" * 50)
    
    results = {}
    
    # 1. Server check
    results['server'] = check_server()
    
    # 2. Integration mock test
    results['integration_mock'] = run_command(
        "python test_integration_mock.py", 
        "Integration Mock Test"
    )
    
    # 3. Fresh test (basic connectivity)
    results['fresh_test'] = run_command(
        "python fresh_test.py", 
        "Fresh Test (Basic Connectivity)"
    )
    
    # 4. Enhanced mock test
    results['enhanced_mock'] = run_command(
        "python enhanced_mock_test.py", 
        "Enhanced Mock Test (Context Optimization)"
    )
    
    # 5. Integration test with custom runner
    results['integration_nav'] = run_command(
        "python run_integration_test.py", 
        "Integration Navigation Test"
    )
    
    # 6. Full YAML test suite
    results['yaml_tests'] = run_command(
        "python yaml_runner.py", 
        "Full YAML Test Suite",
        60
    )
    
    # Results summary
    print("\n" + "=" * 60)
    print("📊 PHASE 2 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<25} {status}")
    
    print("-" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Phase 2 complete!")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Review output above.")
    
    return passed_tests == total_tests

def main():
    """Main test launcher."""
    print("🚀 STARTING PHASE 2 TEST EXECUTION")
    print(f"📁 Working Directory: {project_root}")
    print(f"🐍 Python: {sys.executable}")
    print("⏰ Timestamp:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    success = run_tests()
    
    print(f"\n🏁 Phase 2 Testing {'COMPLETE' if success else 'INCOMPLETE'}")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
