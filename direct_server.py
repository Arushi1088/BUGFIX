#!/usr/bin/env python3
"""
Direct Server - Minimal Flask server inline
"""

import os
import sys
from pathlib import Path

# Change to project directory
project_dir = Path("/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer")
os.chdir(project_dir)

# Add to Python path
sys.path.insert(0, str(project_dir))

print("🌐 Starting Direct Flask Server...")
print(f"📁 Directory: {project_dir}")

try:
    from flask import Flask, send_from_directory, jsonify
    
    app = Flask(__name__, static_folder='.')
    
    @app.route('/')
    def index():
        return '''
<!DOCTYPE html>
<html>
<head><title>Office Mocks Server</title></head>
<body>
    <h1>🌐 Office Mocks Server</h1>
    <h2>📱 Available Mocks:</h2>
    <p><a href="/mocks/word.html">📄 Word Mock</a></p>
    <p><a href="/mocks/excel.html">📊 Excel Mock</a></p>
    <p><a href="/mocks/powerpoint.html">📑 PowerPoint Mock</a></p>
    <p><a href="/health">🩺 Health Check</a></p>
</body>
</html>
        '''
    
    @app.route('/mocks/<path:filename>')
    def serve_mock(filename):
        try:
            return send_from_directory('mocks', filename)
        except FileNotFoundError:
            return f"Mock file '{filename}' not found", 404
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'server': 'Office Mocks'})
    
    print("🚀 Server starting on http://localhost:8000")
    print("📄 Word Mock: http://localhost:8000/mocks/word.html")
    print("📊 Excel Mock: http://localhost:8000/mocks/excel.html")
    print("📑 PowerPoint Mock: http://localhost:8000/mocks/powerpoint.html")
    print("✨ Ready!")
    
    app.run(host='127.0.0.1', port=8000, debug=False)
    
except Exception as e:
    print(f"❌ Server failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
