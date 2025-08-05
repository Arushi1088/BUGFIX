#!/usr/bin/env python3
"""Test script to verify the UX analyzer setup without requiring API calls."""

import os
import sys
import json
import base64

# Test imports
try:
    from computers.default.local_playwright import LocalPlaywrightBrowser
    print("✅ LocalPlaywrightBrowser import successful")
except ImportError as e:
    print(f"❌ Failed to import LocalPlaywrightBrowser: {e}")
    sys.exit(1)

try:
    from agent.agent import Agent
    print("✅ Agent import successful")
except ImportError as e:
    print(f"❌ Failed to import Agent: {e}")
    sys.exit(1)

# Test checklist loading
try:
    with open("uiux_checklist.json") as f:
        checklist = json.load(f)
    print(f"✅ Checklist loaded with {len(checklist)} categories")
    
    # Show checklist structure
    for category, items in checklist.items():
        print(f"  - {category}: {len(items)} items")
except Exception as e:
    print(f"❌ Failed to load checklist: {e}")
    sys.exit(1)

# Test screenshot file exists
screenshot_path = "homepage.png"
if os.path.exists(screenshot_path):
    print(f"✅ Screenshot file found: {screenshot_path}")
    
    # Test base64 encoding
    try:
        with open(screenshot_path, "rb") as img:
            b64 = base64.b64encode(img.read()).decode()
        print(f"✅ Screenshot encoded to base64 ({len(b64)} characters)")
    except Exception as e:
        print(f"❌ Failed to encode screenshot: {e}")
else:
    print(f"❌ Screenshot file not found: {screenshot_path}")

print("\n🎉 Setup verification complete!")
print("To run the UX analyzer, set your OpenAI API key:")
print("export OPENAI_API_KEY='your-api-key-here'")
print("python ux_analyzer.py homepage.png")
