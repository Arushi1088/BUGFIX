#!/usr/bin/env python3
"""
🔧 Quick Server Fix
Run this in a Python environment to start the server
"""

# This script can be run directly from VS Code's Python interpreter
# or from any Python environment

import os
import sys
from pathlib import Path

def start_server():
    # Set correct directory
    project_dir = Path("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")
    os.chdir(project_dir)
    
    print("🔧 QUICK SERVER STARTUP")
    print("=" * 25)
    print(f"📁 Directory: {project_dir}")
    
    # Try to import Flask
    try:
        from flask import Flask, send_from_directory, jsonify
    except ImportError:
        print("❌ Flask not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        from flask import Flask, send_from_directory, jsonify
    
    # Create Flask app
    app = Flask(__name__, static_folder='.')
    
    @app.route('/')
    def home():
        return '''
        <h1>🌐 Office Mocks Server - ACTIVE</h1>
        <p>✅ Server is running on port 8000</p>
        <h2>Available Mocks:</h2>
        <ul>
            <li><a href="/mocks/word.html">📄 Word Mock</a></li>
            <li><a href="/mocks/excel.html">📊 Excel Mock</a></li>
            <li><a href="/mocks/powerpoint.html">📑 PowerPoint Mock</a></li>
        </ul>
        '''
    
    @app.route('/mocks/<path:filename>')
    def serve_mock(filename):
        try:
            return send_from_directory('mocks', filename)
        except:
            return f"Mock '{filename}' not found", 404
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'port': 8000})
    
    print("🚀 Starting server...")
    print("🌐 Access at: http://localhost:8000")
    print("📄 Word: http://localhost:8000/mocks/word.html")
    print("📊 Excel: http://localhost:8000/mocks/excel.html")
    print("📑 PowerPoint: http://localhost:8000/mocks/powerpoint.html")
    print("\n✨ Server starting... (Press Ctrl+C to stop)")
    
    # Start server
    app.run(host='127.0.0.1', port=8000, debug=False)

if __name__ == "__main__":
    start_server()
