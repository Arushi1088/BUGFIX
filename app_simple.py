#!/usr/bin/env python3
"""
🌐 UX Analyzer - Simplified Flask Web Application
Direct OpenAI API integration without CUA Agent complexity.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys
import json
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import tempfile
from computers.default.local_playwright import LocalPlaywrightBrowser
from utils import create_response, check_blocklisted_url

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'ux-analyzer-secret-key-change-in-production'

# Set UTF-8 environment variables for consistent encoding
os.environ.setdefault('PYTHONUTF8', '1')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
os.environ.setdefault('LANG', 'en_US.UTF-8')
os.environ.setdefault('LC_ALL', 'en_US.UTF-8')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load UX checklist
def load_checklist():
    """Load the UX checklist from JSON file."""
    try:
        with open('uiux_checklist.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": {}}

def build_prompt(custom_prompt=None):
    """Build the analysis prompt with UX checklist."""
    base_prompt = """You are a UX/UI expert analyzing this screenshot. Please provide a detailed analysis in JSON format with the following structure:

[
  {
    "category": "Visual Design",
    "item": "specific issue or observation",
    "description": "detailed explanation",
    "severity": "low|medium|high"
  }
]

Focus on these key areas:
- Visual Design (typography, color, layout, spacing)
- Navigation (menu structure, breadcrumbs, search)
- Content (readability, hierarchy, organization)
- Accessibility (contrast, alt text, keyboard navigation)
- Mobile Responsiveness (responsive design, touch targets)
- Performance (loading indicators, perceived speed)
- User Experience (flow, feedback, error handling)
- Interaction Design (buttons, forms, interactive elements)
- Information Architecture (content organization, findability)
- Conversion Optimization (call-to-actions, forms, checkout)

Provide specific, actionable insights. Return ONLY the JSON array, no additional text."""

    if custom_prompt:
        return f"{custom_prompt}\n\n{base_prompt}"
    return base_prompt

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def require_api_key():
    """Check if OpenAI API key is configured."""
    if not os.getenv("OPENAI_API_KEY"):
        abort(403, description="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")

def analyze_url_simple(url, custom_prompt=None):
    """Simplified URL analysis using direct OpenAI API calls."""
    try:
        print(f"🔍 Starting simple analysis for: {url}")
        
        # Check if URL is blocked
        check_blocklisted_url(url)
        
        with LocalPlaywrightBrowser() as computer:
            print("📱 Browser created, navigating to URL...")
            computer.goto(url)
            print("📸 Taking screenshot...")
            screenshot_b64 = computer.screenshot()
            print(f"📸 Screenshot captured, size: {len(screenshot_b64)} bytes")
            
            # Build analysis prompt
            prompt = build_prompt(custom_prompt)
            print(f"📝 Prompt built, length: {len(prompt)} chars")
            
            # Get API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OpenAI API key not found")
            
            print("🚀 Calling OpenAI API directly...")
            # Use our working utils function with correct input format
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url", 
                            "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}
                        }
                    ]
                }
            ]
            
            response = create_response(
                model="gpt-4o",
                input=messages,
                max_tokens=2000
            )
            
            if "error" in response:
                raise Exception(response["error"]["message"])
            
            # Extract text from response
            assistant_text = ""
            if "output" in response:
                for item in response["output"]:
                    if item.get("role") == "assistant":
                        for content in item.get("content", []):
                            if content.get("type") == "text":
                                assistant_text += content.get("text", "")
            
            print(f"📊 Analysis complete, response length: {len(assistant_text)} chars")
            print(f"📊 Response preview: {assistant_text[:200]}...")
            return {"status": "success", "data": assistant_text, "screenshot": screenshot_b64}
            
    except Exception as e:
        print(f"❌ Simple analysis error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e), "screenshot": ""}

def analyze_upload_simple(image_path, custom_prompt=None):
    """Simplified upload analysis using direct OpenAI API calls."""
    try:
        print(f"🔍 Starting simple upload analysis for: {image_path}")
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        screenshot_b64 = base64.b64encode(image_data).decode('utf-8')
        print(f"📸 Image loaded, size: {len(screenshot_b64)} bytes")
        
        # Build analysis prompt
        prompt = build_prompt(custom_prompt)
        print(f"📝 Prompt built, length: {len(prompt)} chars")
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key not found")
        
        print("🚀 Calling OpenAI API directly...")
        # Use our working utils function with correct input format
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}
                    }
                ]
            }
        ]
        
        response = create_response(
            model="gpt-4o",
            input=messages,
            max_tokens=2000
        )
        
        if "error" in response:
            raise Exception(response["error"]["message"])
        
        # Extract text from response
        assistant_text = ""
        if "output" in response:
            for item in response["output"]:
                if item.get("role") == "assistant":
                    for content in item.get("content", []):
                        if content.get("type") == "text":
                            assistant_text += content.get("text", "")
        
        print(f"📊 Analysis complete, response length: {len(assistant_text)} chars")
        print(f"📊 Response preview: {assistant_text[:200]}...")
        return {"status": "success", "data": assistant_text, "screenshot": screenshot_b64}
        
    except Exception as e:
        print(f"❌ Upload analysis error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e), "screenshot": ""}

@app.route('/')
def index():
    """Home page with upload form."""
    return render_template('index.html')

@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    """Handle URL analysis with simplified integration."""
    require_api_key()
    
    url = request.form.get('url')
    if not url:
        flash('Please provide a URL to analyze')
        return redirect(url_for('index'))
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        print(f"🎯 Analyzing URL: {url}")
        result = analyze_url_simple(url)
        
        if result["status"] == "error":
            flash(f'URL analysis failed: {result["error"]}')
            return redirect(url_for('index'))
        
        # Parse the response (expecting JSON format)
        issues = []
        issues_by_category = {}
        try:
            response_text = result["data"]
            # Clean up markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
                
            if isinstance(response_text, str):
                # Try to parse as JSON
                issues = json.loads(response_text)
            elif isinstance(result["data"], list):
                issues = result["data"]
            else:
                issues = [{"category": "Analysis", "item": "AI Response", "description": str(result["data"]), "severity": "medium"}]
                
            # Group issues by category
            for issue in issues:
                category = issue.get("category", "Other")
                if category not in issues_by_category:
                    issues_by_category[category] = []
                issues_by_category[category].append(issue)
                
        except json.JSONDecodeError:
            # If not JSON, treat as plain text response
            issues = [{"category": "Analysis", "item": "AI Response", "description": result["data"], "severity": "medium"}]
            issues_by_category = {"Analysis": issues}

        # Calculate severity counts
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        for issue in issues:
            severity = issue.get("severity", "medium")
            if severity in severity_counts:
                severity_counts[severity] += 1

        # Generate report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        screenshot_data = result.get("screenshot", "")
        return render_template('report.html', 
                               issues=issues,
                               issues_by_category=issues_by_category,
                               url=url, 
                               filename=f"URL Analysis: {url}",
                               timestamp=timestamp,
                               total_issues=len(issues),
                               severity_counts=severity_counts,
                               image_data=screenshot_data)  # Include screenshot for URL analysis

    except Exception as e:
        print(f"❌ Error analyzing URL: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error analyzing URL: {str(e)}')
        return redirect(url_for('index'))

@app.route('/analyze/upload', methods=['POST'])
def analyze_upload():
    """Handle file upload analysis with simplified integration."""
    require_api_key()
    
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            print(f"🎯 Analyzing uploaded file: {filepath}")
            result = analyze_upload_simple(filepath)
            
            # Use screenshot from analysis result
            image_data = result.get("screenshot", "")
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if result["status"] == "error":
                flash(f'File analysis failed: {result["error"]}')
                return redirect(url_for('index'))
            
            # Parse the response
            issues = []
            issues_by_category = {}
            try:
                response_text = result["data"]
                # Clean up markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text.replace("```json", "").replace("```", "").strip()
                elif response_text.startswith("```"):
                    response_text = response_text.replace("```", "").strip()
                    
                if isinstance(response_text, str):
                    issues = json.loads(response_text)
                elif isinstance(result["data"], list):
                    issues = result["data"]
                else:
                    issues = [{"category": "Analysis", "item": "AI Response", "description": str(result["data"]), "severity": "medium"}]
                    
                # Group issues by category
                for issue in issues:
                    category = issue.get("category", "Other")
                    if category not in issues_by_category:
                        issues_by_category[category] = []
                    issues_by_category[category].append(issue)
                    
            except json.JSONDecodeError:
                issues = [{"category": "Analysis", "item": "AI Response", "description": result["data"], "severity": "medium"}]
                issues_by_category = {"Analysis": issues}

            # Calculate severity counts
            severity_counts = {"high": 0, "medium": 0, "low": 0}
            for issue in issues:
                severity = issue.get("severity", "medium")
                if severity in severity_counts:
                    severity_counts[severity] += 1

            # Generate report  
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template('report.html', 
                                   issues=issues,
                                   issues_by_category=issues_by_category,
                                   filename=filename, 
                                   timestamp=timestamp,
                                   total_issues=len(issues),
                                   severity_counts=severity_counts,
                                   image_data=image_data)

        except Exception as e:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"❌ Error analyzing upload: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error analyzing file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint."""
    api_key_configured = bool(os.getenv("OPENAI_API_KEY"))
    checklist_exists = os.path.exists('uiux_checklist.json')
    
    return jsonify({
        'status': 'healthy',
        'api_key_configured': api_key_configured,
        'checklist_loaded': checklist_exists,
        'upload_folder': os.path.exists(UPLOAD_FOLDER)
    })

if __name__ == '__main__':
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
    
    print("🚀 Starting UX Analyzer Web Application (Simplified)...")
    print("📍 Visit: http://127.0.0.1:5001")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(host="0.0.0.0", port=5001, debug=True)
