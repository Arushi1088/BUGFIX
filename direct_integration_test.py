#!/usr/bin/env python3
"""
Direct execution of Integration Nav test
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    print("🎯 DIRECT EXECUTION: Integration Nav Test")
    print("=" * 50)
    
    # Import and run yaml_runner with filter
    try:
        # Simulate command line args for filter
        sys.argv = ['yaml_runner.py', '--filter', 'Integration Nav']
        
        # Import and run
        from yaml_runner import main as yaml_main
        yaml_main()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
