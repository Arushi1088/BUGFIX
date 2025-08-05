#!/usr/bin/env python3
"""
🚀 Quick Test Server
Minimal Flask server to test connectivity
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>🌐 Test Server Running!</h1>
    <p>✅ Flask server is working on port 8080</p>
    <p><a href="/mocks/word.html">Word Mock</a></p>
    <p><a href="/mocks/excel.html">Excel Mock</a></p>
    <p><a href="/mocks/powerpoint.html">PowerPoint Mock</a></p>
    '''

@app.route('/mocks/<filename>')
def serve_mock(filename):
    try:
        with open(f'mocks/{filename}', 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Mock file '{filename}' not found", 404

if __name__ == '__main__':
    print("🚀 Starting test server on port 8080...")
    app.run(host='127.0.0.1', port=8080, debug=False)
