#!/usr/bin/env python3
"""
🎯 Run Integration Nav Test
Executes: python yaml_runner.py --filter "Integration Nav"
"""

import subprocess
import sys
import os

def main():
    print("🎯 RUNNING INTEGRATION NAV TEST")
    print("=" * 40)
    print("Command: python yaml_runner.py --filter 'Integration Nav'")
    print("Working Directory:", os.getcwd())
    print("-" * 40)
    
    try:
        # Run the command
        result = subprocess.run([
            sys.executable, 
            "yaml_runner.py", 
            "--filter", 
            "Integration Nav"
        ], capture_output=True, text=True, timeout=120)
        
        print("📝 STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ STDERR:")
            print(result.stderr)
        
        print(f"\n📊 Return Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Integration Nav test completed successfully!")
        else:
            print("❌ Integration Nav test failed!")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out after 120 seconds")
        return False
    except FileNotFoundError:
        print("❌ yaml_runner.py not found in current directory")
        return False
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
