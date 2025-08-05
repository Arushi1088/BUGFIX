#!/usr/bin/env python3
"""
Mock Office applications server for Phase 3 testing
"""
import http.server
import socketserver
import json
import time
from pathlib import Path

PORT = 8000

class MockOfficeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with mock Office app responses"""

        # Add delay for performance testing
        if "slow" in self.path:
            time.sleep(3)  # Simulate slow loading

        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_index_page().encode())

        elif self.path == "/word.html" or self.path == "/word":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_word_app().encode())

        elif self.path == "/excel.html" or self.path == "/excel":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_excel_app().encode())

        elif self.path == "/powerpoint.html" or self.path == "/powerpoint":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_powerpoint_app().encode())

        elif self.path == "/integration.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_integration_page().encode())

        else:
            super().do_GET()

    def get_index_page(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Office Integration Hub</title>
    <style>
        body { font-family: Segoe UI, Arial, sans-serif; margin: 40px; }
        .app-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .app-card { background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center; }
        .app-card a { text-decoration: none; color: #0078d4; font-size: 18px; }
    </style>
</head>
<body>
    <h1>🏢 Office Integration Hub</h1>
    <div class="app-grid">
        <div class="app-card">
            <h3>📝 Word</h3>
            <a href="/word.html">Open Word App</a>
        </div>
        <div class="app-card">
            <h3>📊 Excel</h3>
            <a href="/excel.html">Open Excel App</a>
        </div>
        <div class="app-card">
            <h3>📽️ PowerPoint</h3>
            <a href="/powerpoint.html">Open PowerPoint App</a>
        </div>
    </div>
</body>
</html>"""

    def get_word_app(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Word - Phase 3 Test</title>
    <style>
        body { font-family: Segoe UI, Arial, sans-serif; margin: 0; }
        .ribbon { background: #0078d4; color: white; padding: 10px 20px; }
        .nav-item { display: inline-block; margin: 0 10px; cursor: pointer; }
        .content { padding: 20px; }
        .document { background: white; min-height: 400px; border: 1px solid #ccc; padding: 20px; }
    </style>
</head>
<body>
    <div class="ribbon">
        <span class="nav-item" data-testid="integration-nav">🔗 Integration</span>
        <span class="nav-item">📄 File</span>
        <span class="nav-item">✏️ Edit</span>
        <span class="nav-item">🎨 Format</span>
    </div>
    <div class="content" data-testid="word-app">
        <h2>Microsoft Word</h2>
        <div class="document">
            <h3>Document Title</h3>
            <p>This is a mock Word document for Phase 3 UX testing.</p>
            <button type="button">Format Text</button>
            <input type="text" placeholder="Search document" />
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzAwNzhkNCIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+SW1hZ2U8L3RleHQ+PC9zdmc+" alt="Document illustration" />
        </div>
    </div>

    <script>
        // Add integration navigation
        document.querySelector('[data-testid="integration-nav"]').addEventListener('click', function() {
            window.location.href = '/integration.html';
        });

        // Performance monitoring
        window.addEventListener('load', function() {
            console.log('Word app loaded');
        });
    </script>
</body>
</html>"""

    def get_excel_app(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Excel - Phase 3 Test</title>
    <style>
        body { font-family: Segoe UI, Arial, sans-serif; margin: 0; }
        .ribbon { background: #107c41; color: white; padding: 10px 20px; }
        .nav-item { display: inline-block; margin: 0 10px; cursor: pointer; }
        .content { padding: 20px; }
        .spreadsheet { background: white; border: 1px solid #ccc; }
        .cell { border: 1px solid #ddd; padding: 8px; display: inline-block; width: 80px; }
    </style>
</head>
<body>
    <div class="ribbon">
        <span class="nav-item" data-testid="integration-nav">🔗 Integration</span>
        <span class="nav-item">📊 Data</span>
        <span class="nav-item">📈 Charts</span>
        <span class="nav-item">🧮 Formulas</span>
    </div>
    <div class="content" data-testid="excel-app">
        <h2>Microsoft Excel</h2>
        <div class="spreadsheet">
            <div class="cell">A1</div>
            <div class="cell">B1</div>
            <div class="cell">C1</div>
            <br>
            <div class="cell">Data</div>
            <div class="cell">100</div>
            <div class="cell">=SUM(B1)</div>
        </div>
        <button type="button">Create Chart</button>
        <select>
            <option>Chart Type</option>
            <option>Bar Chart</option>
            <option>Line Chart</option>
        </select>
        <a href="#help">Help</a>
    </div>

    <script>
        document.querySelector('[data-testid="integration-nav"]').addEventListener('click', function() {
            window.location.href = '/integration.html';
        });
    </script>
</body>
</html>"""

    def get_powerpoint_app(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>PowerPoint - Phase 3 Test</title>
    <style>
        body { font-family: Segoe UI, Arial, sans-serif; margin: 0; }
        .ribbon { background: #d24726; color: white; padding: 10px 20px; }
        .nav-item { display: inline-block; margin: 0 10px; cursor: pointer; }
        .content { padding: 20px; }
        .slide { background: white; width: 400px; height: 300px; border: 1px solid #ccc; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="ribbon">
        <span class="nav-item" data-testid="integration-nav">🔗 Integration</span>
        <span class="nav-item">🎨 Design</span>
        <span class="nav-item">🎭 Animations</span>
        <span class="nav-item">📽️ Slideshow</span>
    </div>
    <div class="content" data-testid="powerpoint-app">
        <h2>Microsoft PowerPoint</h2>
        <div class="slide">
            <h3>Slide 1</h3>
            <p>Presentation content here</p>
        </div>
        <button type="button">Add Slide</button>
        <button type="button">Start Slideshow</button>
        <input type="text" placeholder="Add speaker notes" />
    </div>

    <script>
        document.querySelector('[data-testid="integration-nav"]').addEventListener('click', function() {
            window.location.href = '/integration.html';
        });
    </script>
</body>
</html>"""

    def get_integration_page(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Integration Hub</title>
    <style>
        body { font-family: Segoe UI, Arial, sans-serif; margin: 20px; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="success">
        <h2>✅ Integration Successful</h2>
        <p>You have successfully navigated to the integration hub.</p>
    </div>
    <p><a href="/">Return to main hub</a></p>
</body>
</html>"""

if __name__ == "__main__":
    import socketserver

    print(f"🚀 Starting mock Office server on port {PORT}")
    print(f"📊 Available endpoints:")
    print(f"   • http://localhost:{PORT}/ (Main hub)")
    print(f"   • http://localhost:{PORT}/word.html")
    print(f"   • http://localhost:{PORT}/excel.html") 
    print(f"   • http://localhost:{PORT}/powerpoint.html")
    print(f"   • http://localhost:{PORT}/integration.html")

    with socketserver.TCPServer(("", PORT), MockOfficeHandler) as httpd:
        httpd.serve_forever()
