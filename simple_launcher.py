#!/usr/bin/env python3
"""
🚀 Simple Server Launcher
Just start the server and keep it running
"""

import sys
import os

# Change to project directory
os.chdir("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")

# Import and run server
try:
    print("🌐 Starting Office Mocks Server...")
    print("📁 Directory:", os.getcwd())
    print("🔗 URL: http://localhost:8000")
    
    from server import app
    print("✅ Server module loaded")
    
    print("🚀 Starting server on port 8000...")
    app.run(host='127.0.0.1', port=8000, debug=False)
    
except Exception as e:
    print(f"❌ Server failed: {e}")
    sys.exit(1)
