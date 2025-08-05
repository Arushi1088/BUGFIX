#!/usr/bin/env python3
"""
Simple web server to serve Phase 3 dashboard
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
DASHBOARD_DIR = Path(__file__).parent

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def serve_dashboard():
    """Start the dashboard server"""
    os.chdir(DASHBOARD_DIR)
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"🚀 Phase 3 Dashboard Server")
        print(f"📊 Serving at: http://localhost:{PORT}")
        print(f"📁 Directory: {DASHBOARD_DIR}")
        print("\n🎯 Available dashboards:")
        print(f"   • Minimal: http://localhost:{PORT}/minimal_dashboard.html")
        print(f"   • Simple: http://localhost:{PORT}/simple_dashboard.html")
        print(f"   • Full: http://localhost:{PORT}/phase3_sample_dashboard_20250729_203830.html")
        print("\n✨ Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    serve_dashboard()
