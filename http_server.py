#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

os.chdir('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🚀 Server started at http://localhost:{PORT}")
    print(f"📊 Dashboard: http://localhost:{PORT}/minimal_dashboard.html")
    httpd.serve_forever()
