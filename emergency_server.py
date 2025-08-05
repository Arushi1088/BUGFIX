#!/usr/bin/env python3
"""
🔥 Emergency Server Launcher
Simple, direct server startup
"""

import os
import sys

# Navigate to project directory
project_dir = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer"
os.chdir(project_dir)

# Add project to Python path
sys.path.insert(0, project_dir)

print("🚨 EMERGENCY SERVER STARTUP")
print("=" * 35)
print(f"📁 Directory: {project_dir}")

try:
    # Import Flask
    from flask import Flask, send_from_directory, jsonify
    print("✅ Flask imported successfully")
    
    # Create Flask app
    app = Flask(__name__, static_folder='.')
    print("✅ Flask app created")
    
    @app.route('/')
    def home():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Office Mocks Server - RUNNING</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #28a745; }
                .status { background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745; }
                .link { display: block; padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 5px; text-decoration: none; color: #007bff; border-left: 4px solid #007bff; }
                .link:hover { background: #e9ecef; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌐 Office Mocks Server - ACTIVE</h1>
                
                <div class="status">
                    <strong>✅ SERVER STATUS: RUNNING</strong><br>
                    🔗 Port: 8000<br>
                    📅 Started: Successfully<br>
                    🎯 Ready for testing!
                </div>
                
                <h2>📱 Office Application Mocks</h2>
                <a href="/mocks/word.html" class="link">📄 Microsoft Word Mock</a>
                <a href="/mocks/excel.html" class="link">📊 Microsoft Excel Mock</a>
                <a href="/mocks/powerpoint.html" class="link">📑 Microsoft PowerPoint Mock</a>
                
                <h2>🔧 Server Endpoints</h2>
                <a href="/health" class="link">🩺 Health Check</a>
                <a href="/status" class="link">📊 Server Status</a>
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
            return f'''
            <h1>❌ Mock Not Found</h1>
            <p>The requested mock file '{filename}' was not found.</p>
            <p><a href="/">← Back to Home</a></p>
            ''', 404
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'server': 'Office Mocks Server',
            'port': 8000,
            'message': 'Server is running successfully!',
            'available_mocks': ['word.html', 'excel.html', 'powerpoint.html']
        })
    
    @app.route('/status')
    def status():
        """Server status endpoint."""
        return jsonify({
            'server_status': 'running',
            'working_directory': os.getcwd(),
            'python_version': sys.version,
            'flask_app': 'active',
            'timestamp': 'July 29, 2025'
        })
    
    # Print startup info
    print("✅ Routes configured:")
    print("   🏠 Home: /")
    print("   📄 Word Mock: /mocks/word.html")
    print("   📊 Excel Mock: /mocks/excel.html")
    print("   📑 PowerPoint Mock: /mocks/powerpoint.html")
    print("   🩺 Health: /health")
    print("   📊 Status: /status")
    
    print("\n🚀 Starting server on http://localhost:8000...")
    print("🌐 You can access the server at:")
    print("   http://localhost:8000")
    print("   http://127.0.0.1:8000")
    
    # Start the server
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=8000,
        debug=False,
        threaded=True,
        use_reloader=False
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try: pip install flask")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Server startup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
