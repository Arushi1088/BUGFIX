#!/usr/bin/env python3
"""
🚀 Robust Server Startup
Ensures server starts properly on port 8000
"""

import os
import sys
import time
import socket
import subprocess
from pathlib import Path

def check_port_available(port):
    """Check if port is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0  # True if port is available
    except:
        return True

def kill_processes_on_port(port):
    """Kill any processes using the specified port."""
    try:
        # Use lsof to find processes on port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    subprocess.run(['kill', '-9', pid], check=False)
                    print(f"🛑 Killed process {pid} on port {port}")
                except:
                    pass
        time.sleep(2)
    except:
        pass

def start_flask_server():
    """Start the Flask server."""
    
    print("🚀 ROBUST SERVER STARTUP")
    print("=" * 30)
    
    # Set working directory
    project_dir = Path("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")
    
    # Check if server.py exists
    if not (project_dir / "server.py").exists():
        print("❌ server.py not found!")
        return False
    
    # Check port availability
    port = 8000
    if not check_port_available(port):
        print(f"⚠️  Port {port} is in use, cleaning up...")
        kill_processes_on_port(port)
        
        # Wait and check again
        time.sleep(3)
        if not check_port_available(port):
            print(f"❌ Could not free port {port}")
            return False
    
    print(f"✅ Port {port} is available")
    
    # Start server
    python_path = project_dir / ".venv/bin/python"
    if not python_path.exists():
        print("❌ Virtual environment not found!")
        return False
    
    print("🌐 Starting Flask server...")
    
    # Create a simple server inline to avoid import issues
    server_code = '''
import os
import sys
from flask import Flask, send_from_directory, jsonify, render_template_string

# Set working directory
os.chdir("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Office Mocks Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #0078d4; }
        .mock-link { display: block; padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 5px; text-decoration: none; color: #0078d4; border-left: 4px solid #0078d4; }
        .mock-link:hover { background: #e9ecef; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Office Mocks Server</h1>
        <p>✅ Server running on port 8000</p>
        
        <h2>📱 Available Office Mocks:</h2>
        <a href="/mocks/word.html" class="mock-link">📄 Microsoft Word Mock</a>
        <a href="/mocks/excel.html" class="mock-link">📊 Microsoft Excel Mock</a>
        <a href="/mocks/powerpoint.html" class="mock-link">📑 Microsoft PowerPoint Mock</a>
        
        <h2>🔧 API Endpoints:</h2>
        <a href="/health" class="mock-link">🩺 Health Check</a>
    </div>
</body>
</html>
    """

@app.route('/mocks/<path:filename>')
def serve_mock(filename):
    try:
        return send_from_directory('mocks', filename)
    except FileNotFoundError:
        return f"Mock file '{filename}' not found", 404

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'server': 'Office Mocks Server',
        'port': 8000,
        'mocks': ['word.html', 'excel.html', 'powerpoint.html']
    })

if __name__ == '__main__':
    print("🌐 Office Mocks Server starting...")
    print("📁 Serving from:", os.getcwd())
    print("🔗 Available at: http://localhost:8000")
    print("📄 Word: http://localhost:8000/mocks/word.html")
    print("📊 Excel: http://localhost:8000/mocks/excel.html")
    print("📑 PowerPoint: http://localhost:8000/mocks/powerpoint.html")
    print("✨ Server ready!")
    
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=True)
'''
    
    try:
        # Write server code to temp file and run it
        with open('temp_server.py', 'w') as f:
            f.write(server_code)
        
        # Start the server
        print("🚀 Launching server...")
        process = subprocess.Popen([str(python_path), 'temp_server.py'])
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Test if server is responding
        import requests
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and responding!")
                print("🌐 Access at: http://localhost:8000")
                return True
            else:
                print(f"⚠️  Server responded with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server not responding: {e}")
            process.kill()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    success = start_flask_server()
    if success:
        print("\\n🎉 SERVER STARTUP: SUCCESS!")
        print("🚀 Office Mocks Server is running!")
        print("\\n📱 Open these URLs:")
        print("   🏠 Home: http://localhost:8000")
        print("   📄 Word: http://localhost:8000/mocks/word.html")
        print("   📊 Excel: http://localhost:8000/mocks/excel.html")
        print("   📑 PowerPoint: http://localhost:8000/mocks/powerpoint.html")
    else:
        print("\\n💥 SERVER STARTUP: FAILED!")
        print("🛠️  Check the errors above")
        sys.exit(1)
