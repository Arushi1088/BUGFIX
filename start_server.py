#!/usr/bin/env python3
"""
🔧 Server Starter - Robust Flask Server
Ensures Office mocks server starts reliably
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def check_port(port):
    """Check if a port is available."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0  # True if port is in use
    except:
        return False

def start_server():
    """Start the Flask server with error handling."""
    
    print("🔧 OFFICE MOCKS SERVER STARTER")
    print("=" * 40)
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Check for required files
    required_files = ['server.py', 'mocks/word.html', 'mocks/excel.html', 'mocks/powerpoint.html']
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    
    # Check if port 8000 is already in use
    if check_port(8000):
        print("⚠️  Port 8000 is already in use")
        print("🔄 Attempting to use existing server...")
        
        try:
            response = requests.get("http://localhost:8000", timeout=3)
            if response.status_code == 200:
                print("✅ Existing server is working!")
                return True
        except:
            print("❌ Existing server not responding")
            
        # Try to kill existing process
        print("🛑 Stopping existing process...")
        os.system("lsof -ti:8000 | xargs kill -9 2>/dev/null")
        time.sleep(2)
    
    # Start the server
    print("🚀 Starting Flask server...")
    
    python_path = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/.venv/bin/python"
    
    try:
        # Start server as background process
        process = subprocess.Popen([
            python_path, "server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Test if server is responding
        for attempt in range(5):
            try:
                response = requests.get("http://localhost:8000", timeout=2)
                if response.status_code == 200:
                    print("✅ Server started successfully!")
                    print("🌐 Available at: http://localhost:8000")
                    print("📄 Word Mock: http://localhost:8000/mocks/word.html")
                    print("📊 Excel Mock: http://localhost:8000/mocks/excel.html")
                    print("📑 PowerPoint Mock: http://localhost:8000/mocks/powerpoint.html")
                    return True
            except:
                print(f"⏳ Attempt {attempt + 1}/5 - Server starting...")
                time.sleep(2)
        
        print("❌ Server failed to respond after 5 attempts")
        
        # Check process status
        if process.poll() is None:
            print("🔄 Process is running but not responding")
            stdout, stderr = process.communicate(timeout=5)
            if stderr:
                print(f"🚨 Server errors: {stderr.decode()}")
        else:
            print("💥 Process terminated unexpectedly")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"🚨 Server errors: {stderr.decode()}")
        
        return False
        
    except Exception as e:
        print(f"💥 Failed to start server: {e}")
        return False

def open_browser_tabs():
    """Open the mocks in browser tabs."""
    print("\\n🌐 Opening browser tabs...")
    
    urls = [
        "http://localhost:8000",
        "http://localhost:8000/mocks/word.html",
        "http://localhost:8000/mocks/excel.html", 
        "http://localhost:8000/mocks/powerpoint.html"
    ]
    
    for url in urls:
        try:
            # We would use VS Code's Simple Browser here in real scenario
            print(f"📱 Open: {url}")
        except Exception as e:
            print(f"⚠️  Could not open {url}: {e}")

if __name__ == "__main__":
    success = start_server()
    
    if success:
        print("\\n🎉 SERVER STARTUP: SUCCESS!")
        print("🔗 Office Mocks Server is running on http://localhost:8000")
        open_browser_tabs()
    else:
        print("\\n💥 SERVER STARTUP: FAILED!")
        print("🛠️  Try manual startup: python server.py")
        sys.exit(1)
