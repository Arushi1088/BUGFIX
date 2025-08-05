#!/usr/bin/env python3
"""
🌐 Test Web Server Setup
Creates a simple test page and starts server on port 8080 for testing.
"""

import os
import http.server
import socketserver
import threading
import time

def create_test_page():
    """Create a simple test page for UX testing."""
    
    test_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UX Test Page - Phase 1 Enhanced System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .search-section {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .form-section {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        input[type="text"], input[type="email"], textarea {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .navigation {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        .nav-link {
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            color: white;
            transition: background 0.3s;
        }
        .nav-link:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        .results {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 UX Testing Page - Phase 1 Enhanced System</h1>
        <p>This page tests the enhanced UX analyzer with batching, disambiguation, and rate limiting.</p>
        
        <!-- Navigation Section (tests navigation batching) -->
        <div class="navigation">
            <a href="#search" class="nav-link" onclick="showSection('search')">Search</a>
            <a href="#contact" class="nav-link" onclick="showSection('contact')">Contact</a>
            <a href="#about" class="nav-link" onclick="showSection('about')">About</a>
            <a href="#products" class="nav-link" onclick="showSection('products')">Products</a>
        </div>
        
        <!-- Search Section (tests find_elements and disambiguation) -->
        <div id="search-section" class="search-section">
            <h2>🔍 Search Functionality</h2>
            <p>Test batching optimization: find_elements → fill → click → screenshot</p>
            
            <!-- Multiple search inputs to test disambiguation -->
            <input type="text" id="main-search" name="search" placeholder="Main search (primary)" class="search-input">
            <input type="text" id="quick-search" name="search" placeholder="Quick search (secondary)" class="search-input">
            <input type="text" id="advanced-search" name="search" placeholder="Advanced search (tertiary)" class="search-input">
            
            <button onclick="performSearch()" class="search-btn">Search</button>
            <button onclick="performSearch()" class="search-button">Alternative Search</button>
            
            <div id="search-results" class="results hidden">
                <h3>Search Results</h3>
                <p>Results for: <span id="search-term"></span></p>
                <ul>
                    <li>Enhanced UX Testing with AI</li>
                    <li>Automated Browser Interactions</li>
                    <li>Rate Limiting and Retry Logic</li>
                    <li>Smart Element Disambiguation</li>
                    <li>Batching Optimization Techniques</li>
                </ul>
            </div>
        </div>
        
        <!-- Contact Form Section (tests form field batching) -->
        <div id="contact-section" class="form-section">
            <h2>📝 Contact Form</h2>
            <p>Test form batching: gather fields → fill multiple → screenshot</p>
            
            <form id="contact-form">
                <input type="text" id="name" name="name" placeholder="Your Name" required>
                <input type="email" id="email" name="email" placeholder="Your Email" required>
                <input type="text" id="company" name="company" placeholder="Company (optional)">
                <textarea id="message" name="message" placeholder="Your Message" rows="4" required></textarea>
                
                <!-- Multiple submit buttons to test disambiguation -->
                <button type="button" onclick="submitForm()" class="submit-btn">Send Message</button>
                <button type="button" onclick="submitForm()" class="contact-submit">Submit Contact</button>
            </form>
            
            <div id="form-success" class="results hidden">
                <h3>✅ Message Sent Successfully!</h3>
                <p>Thank you for testing the enhanced UX system.</p>
            </div>
        </div>
        
        <!-- Dynamic Content Section -->
        <div id="dynamic-section" class="form-section">
            <h2>⚡ Dynamic Content</h2>
            <p>Test wait_for_element and dynamic loading</p>
            
            <button onclick="loadDynamicContent()" class="load-btn">Load Dynamic Content</button>
            <button onclick="loadDynamicContent()" class="dynamic-loader">Alternative Loader</button>
            
            <div id="dynamic-content" class="results hidden">
                <h3>🎉 Dynamic Content Loaded!</h3>
                <p>This content was loaded dynamically to test wait_for_element functionality.</p>
                <ul>
                    <li>Phase 1: Rate limiting ✅</li>
                    <li>Phase 1: Disambiguation ✅</li>
                    <li>Phase 1: Batching ✅</li>
                    <li>System Status: Enhanced and Ready 🚀</li>
                </ul>
            </div>
        </div>
        
        <!-- Test Results Display -->
        <div id="test-results" class="results">
            <h3>🧪 Test Instructions</h3>
            <p><strong>Expected Batching Behaviors:</strong></p>
            <ul>
                <li><strong>Search Test:</strong> find_elements → fill → click → screenshot</li>
                <li><strong>Form Test:</strong> gather all fields → fill multiple → screenshot</li>
                <li><strong>Navigation:</strong> click → wait_for_element → screenshot</li>
                <li><strong>Dynamic:</strong> click → wait_for_element → screenshot</li>
            </ul>
            
            <p><strong>Disambiguation Tests:</strong></p>
            <ul>
                <li>Multiple search inputs with same name/type</li>
                <li>Multiple submit buttons with different classes</li>
                <li>Similar elements requiring smart selection</li>
            </ul>
        </div>
    </div>
    
    <script>
        function performSearch() {
            const searchInputs = document.querySelectorAll('.search-input');
            let searchTerm = '';
            
            // Find the input with content
            for (let input of searchInputs) {
                if (input.value.trim()) {
                    searchTerm = input.value.trim();
                    break;
                }
            }
            
            if (!searchTerm) {
                searchTerm = 'AI and UX Testing';
                document.getElementById('main-search').value = searchTerm;
            }
            
            document.getElementById('search-term').textContent = searchTerm;
            document.getElementById('search-results').classList.remove('hidden');
        }
        
        function submitForm() {
            const form = document.getElementById('contact-form');
            const formData = new FormData(form);
            
            // Simulate form submission
            setTimeout(() => {
                document.getElementById('form-success').classList.remove('hidden');
            }, 500);
        }
        
        function loadDynamicContent() {
            // Simulate loading delay
            setTimeout(() => {
                document.getElementById('dynamic-content').classList.remove('hidden');
            }, 1000);
        }
        
        function showSection(section) {
            // Simple navigation simulation
            console.log('Navigating to:', section);
        }
    </script>
</body>
</html>'''
    
    # Write the test page
    with open('test_page.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test page created: test_page.html")

def start_web_server(port=8080):
    """Start a simple web server on the specified port."""
    
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress log messages for cleaner output
            pass
    
    try:
        with socketserver.TCPServer(("", port), QuietHTTPRequestHandler) as httpd:
            print(f"🌐 Web server started on http://localhost:{port}")
            print(f"📄 Test page: http://localhost:{port}/test_page.html")
            print("🛑 Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try: lsof -ti:{port} | xargs kill")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    print("🌐 SETTING UP TEST WEB SERVER")
    print("=" * 40)
    
    # Create test page
    create_test_page()
    
    # Start server
    start_web_server(8080)
