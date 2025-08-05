#!/usr/bin/env python3
"""
🚀 Manual Smoke Test Runner
Step-by-step comprehensive testing
"""

import os
import sys
import subprocess
import time
import requests

def run_step(step_name, command, description):
    """Run a test step and report results."""
    print(f"\n{'='*50}")
    print(f"🔧 {step_name}: {description}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {step_name} PASSED")
            if result.stdout:
                print("📊 Output:")
                # Show last few lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[-10:]:  # Last 10 lines
                    print(f"   {line}")
            return True
        else:
            print(f"❌ {step_name} FAILED")
            if result.stderr:
                print("🚨 Error:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {step_name} TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {step_name} EXCEPTION: {e}")
        return False

def check_server():
    """Check if server is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """Run comprehensive smoke test."""
    
    print("🎯 MANUAL COMPREHENSIVE SMOKE TEST")
    print("=" * 50)
    
    # Change to project directory
    project_dir = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer"
    os.chdir(project_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    python_cmd = f"{project_dir}/.venv/bin/python"
    
    # Start server
    print("\n🌐 Starting server...")
    server_process = subprocess.Popen([python_cmd, "server.py"])
    
    # Wait for server
    print("⏳ Waiting for server startup...")
    for i in range(10):
        if check_server():
            print("✅ Server is running!")
            break
        time.sleep(1)
        print(f"   Attempt {i+1}/10...")
    else:
        print("❌ Server failed to start")
        server_process.kill()
        return False
    
    # Test steps
    steps = [
        ("Quick Test", f"{python_cmd} tests/quick_mock_test.py", "Quick connectivity check"),
        ("Word Test", f"{python_cmd} tests/verify_word_mock.py", "Word mock verification"),
        ("Excel Test", f"{python_cmd} tests/verify_excel_mock.py", "Excel mock verification"),
        ("PowerPoint Test", f"{python_cmd} tests/verify_powerpoint_mock.py", "PowerPoint mock verification"),
    ]
    
    results = {}
    
    for step_name, command, description in steps:
        results[step_name] = run_step(step_name, command, description)
    
    # YAML test
    print(f"\n{'='*50}")
    print("🧪 YAML System Test")
    print('='*50)
    
    try:
        yaml_test = f"""
import yaml
print('Testing YAML system...')
with open('schemas/office_tests.yaml', 'r') as f:
    data = yaml.safe_load(f)
print(f'✅ YAML schema loaded: {{len(data.get("tests", []))}} tests')
from yaml_runner import YAMLTestRunner
print('✅ YAMLTestRunner imported successfully')
"""
        result = subprocess.run([python_cmd, "-c", yaml_test], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ YAML System PASSED")
            print("📊 Output:")
            print(result.stdout)
            results["YAML Test"] = True
        else:
            print("❌ YAML System FAILED")
            print(result.stderr)
            results["YAML Test"] = False
    except Exception as e:
        print(f"💥 YAML System EXCEPTION: {e}")
        results["YAML Test"] = False
    
    # Cleanup
    print(f"\n{'='*50}")
    print("🧹 Cleanup")
    print('='*50)
    server_process.kill()
    print("✅ Server stopped")
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 SMOKE TEST RESULTS SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        icon = "✅" if success else "❌"
        status = "PASSED" if success else "FAILED"
        print(f"{icon} {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌟 ALL TESTS PASSED! Office mocks are fully operational!")
        return True
    else:
        print("🔧 Some tests failed - check individual results above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
