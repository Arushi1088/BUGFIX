#!/usr/bin/env python3
"""
🌐 Flask Test - UX Analyzer
Simple test to verify Flask installation and basic functionality.
"""

from flask import Flask

# Create Flask app
app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <h1>🎉 Flask is Working!</h1>
    <p>UX Analyzer Flask installation successful.</p>
    <p><strong>Next steps:</strong></p>
    <ul>
        <li>✅ Flask 3.1.1 installed</li>
        <li>✅ Virtual environment active</li>
        <li>✅ Ready for web development</li>
    </ul>
    <p><a href="/test">Test Route</a></p>
    """

@app.route('/test')
def test():
    return """
    <h2>🔧 Test Route</h2>
    <p>This is a test route to verify Flask routing works.</p>
    <p><a href="/">← Back to Home</a></p>
    """

if __name__ == '__main__':
    print("🚀 Starting Flask test server...")
    print("📍 Visit: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    app.run(debug=True, host='localhost', port=5000)
