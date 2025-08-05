#!/usr/bin/env python3
"""
🎯 Quick Test Runner - In correct directory
"""

import os
import sys
import subprocess

print("🎯 QUICK TEST RUNNER")
print(f"📁 Current directory: {os.getcwd()}")

# We're already in the right directory, just run the test
try:
    result = subprocess.run([sys.executable, "fresh_test.py"], 
                          capture_output=False, 
                          text=True)
    if result.returncode == 0:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test had issues")
except Exception as e:
    print(f"❌ Error running test: {e}")
