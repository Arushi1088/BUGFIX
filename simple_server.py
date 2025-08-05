#!/usr/bin/env python3
"""
🚀 Simple Server Starter
Quick Flask server for Office mocks testing
"""

from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Office Mocks Server - Running</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #0078d4; }
        .link-box { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #0078d4; }
        a { color: #0078d4; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Office Mocks Server</h1>
        <p>✅ Server is running successfully on port 8000!</p>
        
        <h2>📱 Available Office Mocks:</h2>
        
        <div class="link-box">
            <h3>📄 Microsoft Word Mock</h3>
            <a href="/mocks/word.html">→ Open Word Mock</a>
        </div>
        
        <div class="link-box">
            <h3>📊 Microsoft Excel Mock</h3>
            <a href="/mocks/excel.html">→ Open Excel Mock</a>
        </div>
        
        <div class="link-box">
            <h3>📑 Microsoft PowerPoint Mock</h3>
            <a href="/mocks/powerpoint.html">→ Open PowerPoint Mock</a>
        </div>
        
        <h2>🔧 API Endpoints:</h2>
        <div class="link-box">
            <a href="/health">→ Health Check</a><br>
            <a href="/api/mock-status">→ Mock Status</a>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/mocks/<path:filename>')
def serve_mock(filename):
    """Serve mock files from mocks directory."""
    try:
        return send_from_directory('mocks', filename)
    except FileNotFoundError:
        return f"Mock file '{filename}' not found", 404

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'server': 'Office Mocks Server',
        'port': 8000,
        'mocks_available': ['word.html', 'excel.html', 'powerpoint.html']
    })

@app.route('/api/mock-status')
def mock_status():
    """Status of available mocks."""
    mocks_dir = 'mocks'
    available_mocks = []
    
    if os.path.exists(mocks_dir):
        for filename in os.listdir(mocks_dir):
            if filename.endswith('.html'):
                available_mocks.append(filename)
    
    return jsonify({
        'status': 'operational',
        'available_mocks': available_mocks,
        'total_mocks': len(available_mocks)
    })

if __name__ == '__main__':
    print("🌐 Starting Office Mocks Server...")
    print("📁 Serving mocks from: ./mocks/")
    print("🔗 Available at: http://localhost:8000")
    print("📄 Word Mock: http://localhost:8000/mocks/word.html")
    print("📊 Excel Mock: http://localhost:8000/mocks/excel.html")
    print("📑 PowerPoint Mock: http://localhost:8000/mocks/powerpoint.html")
    print("🏠 Home Page: http://localhost:8000")
    print("✨ Ready for Phase 2 testing!")
    
    try:
        app.run(host='127.0.0.1', port=8000, debug=True)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
