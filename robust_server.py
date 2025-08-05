#!/usr/bin/env python3
"""
🌐 Robust Server Startup - FINAL VERSION
Starts Flask server with full error handling and connectivity testing
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def signal_handler(sig, frame):
    print('\n🛑 Server shutdown requested')
    sys.exit(0)

def check_port_available(port=8000):
    """Check if port is available"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # Port is available if connection failed
    except:
        return True

def start_robust_server():
    """Start the server with full error handling"""
    print("🌐 ROBUST FLASK SERVER STARTUP")
    print("=" * 35)
    
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check current directory
    project_dir = Path("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")
    if not project_dir.exists():
        print(f"❌ Project directory not found: {project_dir}")
        return False
        
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")
    
    # Check if port is available
    if not check_port_available(8000):
        print("⚠️ Port 8000 already in use")
        print("💡 To stop existing server: pkill -f 'flask.*8000' or pkill -f 'python.*8000'")
        
        # Try to find and show the existing process
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if '8000' in line and 'python' in line:
                    print(f"🔍 Found: {line.strip()}")
        except:
            pass
            
        choice = input("\n🤔 Continue anyway? (y/N): ").strip().lower()
        if choice != 'y':
            return False
    
    # Check for required files
    required_files = [
        'mocks/word.html',
        'mocks/excel.html', 
        'mocks/powerpoint.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files:")
        for file_path in missing_files:
            print(f"   • {file_path}")
        return False
    
    print("✅ All mock files found")
    
    # Try to import Flask
    try:
        from flask import Flask, send_from_directory, jsonify
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            from flask import Flask, send_from_directory, jsonify
            print("✅ Flask installed and imported")
        except Exception as e:
            print(f"❌ Failed to install Flask: {e}")
            return False
    
    # Create Flask app
    app = Flask(__name__, static_folder='.')
    print("✅ Flask app created")
    
    @app.route('/')
    def home():
        return '''
        <h1>🌐 Office Mocks Server - ROBUST VERSION</h1>
        <p>✅ Server is running on port 8000</p>
        <h2>Available Office Mocks:</h2>
        <ul>
            <li><a href="/mocks/word.html" target="_blank">📄 Word Mock</a></li>
            <li><a href="/mocks/excel.html" target="_blank">📊 Excel Mock</a></li>
            <li><a href="/mocks/powerpoint.html" target="_blank">📑 PowerPoint Mock</a></li>
            <li><a href="/mocks/integration.html" target="_blank">🌐 Integration Hub</a></li>
        </ul>
        <h2>Test Endpoints:</h2>
        <ul>
            <li><a href="/health">🔍 Health Check</a></li>
            <li><a href="/status">📊 Server Status</a></li>
        </ul>
        <p><strong>Ready for InteractiveUXAgent testing!</strong></p>
        '''
    
    @app.route('/mocks/<path:filename>')
    def serve_mock(filename):
        try:
            return send_from_directory('mocks', filename)
        except Exception as e:
            return f"❌ Mock '{filename}' not found: {str(e)}", 404
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'port': 8000,
            'mocks_available': ['word.html', 'excel.html', 'powerpoint.html', 'integration.html'],
            'ready_for_testing': True
        })
    
    @app.route('/status')
    def status():
        return jsonify({
            'server': 'Flask Development Server',
            'port': 8000,
            'project_dir': str(project_dir),
            'mock_files_found': len([f for f in required_files if (project_dir / f).exists()]),
            'uptime': time.time()
        })
    
    print("✅ Routes configured")
    
    # Display startup info
    print("\n🚀 STARTING SERVER...")
    print("📍 URLs:")
    print("   🏠 Home: http://localhost:8000")
    print("   📄 Word: http://localhost:8000/mocks/word.html")
    print("   📊 Excel: http://localhost:8000/mocks/excel.html")
    print("   📑 PowerPoint: http://localhost:8000/mocks/powerpoint.html")
    print("   🔍 Health: http://localhost:8000/health")
    
    print("\n💡 Testing commands:")
    print("   curl http://localhost:8000/health")
    print("   python enhanced_mock_test.py")
    print("   python yaml_runner.py")
    
    print(f"\n✨ Server starting on port 8000...")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Start the server
        app.run(
            host='127.0.0.1', 
            port=8000, 
            debug=False,
            use_reloader=False  # Prevent double startup in debug mode
        )
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎯 Starting Robust Flask Server for Office Mocks...")
    
    try:
        start_robust_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
