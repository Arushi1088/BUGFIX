#!/usr/bin/env python3
"""
🌐 UX Analyzer - Flask Web Application
A web interface for analyzing UI/UX screenshots and web pages using AI's vision model.
"""

from dotenv import load_dotenv
load_dotenv()   # pulls in .env into os.environ

import os
import sys
import json
import base64
import openai
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import tempfile
from computers.default.local_playwright import LocalPlaywrightBrowser
from agent.agent import Agent

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
        # Fallback basic checklist if file not found
        return {
            "Visual Design": ["Typography readability", "Color contrast", "Visual hierarchy"],
            "Navigation": ["Clear navigation structure", "Consistent navigation"],
            "Usability": ["Intuitive interface", "Clear call-to-action buttons"],
            "Accessibility": ["Keyboard navigation", "Screen reader compatibility"],
            "Mobile": ["Responsive design", "Touch-friendly interface"]
        }

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_checklist(checklist):
    """Format checklist for prompt."""
    lines = []
    for category, items in checklist.items():
        lines.append(f"## {category}")
        for item in items:
            lines.append(f"- {item}")
    return "\\n".join(lines)

def build_prompt(custom_prompt=None):
    """Build the analysis prompt using the checklist."""
    checklist = load_checklist()
    
    # Use custom prompt if provided, otherwise use default
    if custom_prompt:
        base_prompt = custom_prompt
    else:
        base_prompt = f"""
You are a UX expert. Analyze the supplied screenshot or webpage using this checklist:
{format_checklist(checklist)}

Return a JSON array of issues, where each issue has:
- category: which checklist section
- item: the specific checklist item  
- description: what's wrong
- severity: "high", "medium", or "low"
- (optional) bbox: [x, y, width, height]
Respond only with valid JSON.
"""
    
    # Comprehensive Unicode sanitization
    import unicodedata
    
    # First normalize to NFKC (canonical decomposition + compatibility + canonical composition)
    prompt = unicodedata.normalize("NFKC", base_prompt)
    
    # Replace problematic Unicode characters that can cause encoding issues
    prompt = prompt.replace("\u2011", "-")  # non-breaking hyphen
    prompt = prompt.replace("\u2012", "-")  # figure dash  
    prompt = prompt.replace("\u2013", "-")  # en dash
    prompt = prompt.replace("\u2014", "-")  # em dash
    prompt = prompt.replace("\u2015", "-")  # horizontal bar
    prompt = prompt.replace("\u2010", "-")  # hyphen
    prompt = prompt.replace("\u00a0", " ")  # non-breaking space
    prompt = prompt.replace("\u202f", " ")  # narrow no-break space
    prompt = prompt.replace("\u2009", " ")  # thin space
    
    # Encode to ASCII and decode back to remove any remaining problematic characters
    prompt = prompt.encode('ascii', errors='ignore').decode('ascii')
    
    return prompt

def analyze_url_direct(url, custom_prompt=None, task=None):
    """Direct analysis using interactive agent for tasks or simple vision for general analysis."""
    try:
        print(f"🔍 Starting analysis for: {url}")
        if task:
            print(f"📋 Task scenario: {task}")
            
            # Use interactive agent for scenario-based testing
            from interactive_agent import InteractiveUXAgent
            agent = InteractiveUXAgent()
            result = agent.analyze_scenario(url, task)
            
            if result["status"] == "success":
                # Extract issues from the final analysis
                issues = result.get("final_analysis", {}).get("issues", [])
                return {"status": "success", "data": issues}
            else:
                return {"status": "error", "error": result.get("error", "Unknown error")}
        
        else:
            # Use simple vision analysis for general UX review
            with LocalPlaywrightBrowser() as computer:
                print("📱 Browser created, setting up page...")
                
                print("📱 Navigating to URL...")
                computer.goto(url)
                print("📸 Taking screenshot...")
                screenshot_b64 = computer.screenshot()
                print(f"📸 Screenshot captured, size: {len(screenshot_b64)} bytes")
                
                # Build analysis prompt
                prompt = build_prompt(custom_prompt)
                print(f"📝 Prompt built, length: {len(prompt)} chars")
                
                # Additional Unicode sanitization for safety
                prompt = prompt.encode('utf-8', errors='ignore').decode('utf-8')
                print(f"🔤 Prompt sanitized")
                
                # Use OpenAI directly for vision analysis
                client = openai.OpenAI()
                print("🤖 Calling OpenAI Vision API...")
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    max_tokens=2000
                )
                
                print("✅ Analysis completed successfully")
                
                # Get the response text
                result_text = response.choices[0].message.content
                print(f"� Response length: {len(result_text)} chars")
                
                return {
                    "status": "success",
                    "data": result_text
                }
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

def analyze_upload_direct(image_path, custom_prompt=None):
    """Direct analysis of uploaded image using OpenAI vision."""
    try:
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        screenshot_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build analysis prompt
        prompt = build_prompt(custom_prompt)
        
        # Use OpenAI directly for vision analysis
        client = openai.OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        # Get the response text
        result_text = response.choices[0].message.content
        
        return {"status": "success", "data": result_text}
        
    except Exception as e:
        print(f"Direct upload analysis error: {e}")
        return {"status": "error", "error": str(e)}

def analyze_screenshot_with_openai(image_path, checklist):
    """Analyze screenshot using OpenAI's vision model."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not configured")
    
    client = openai.OpenAI()
    
    # Read and encode the screenshot
    with open(image_path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    
    prompt = f"""
You are a UX expert. Analyze the supplied screenshot using this checklist:
{format_checklist(checklist)}

Return a JSON array of issues, where each issue has:
- category: which checklist section
- item: the specific checklist item
- description: what's wrong
- severity: "high", "medium", or "low"
- (optional) bbox: [x, y, width, height]
Respond only with valid JSON.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        # Extract and parse response
        assistant_text = response.choices[0].message.content
        
        # Handle markdown code blocks
        if "```json" in assistant_text:
            start = assistant_text.find("```json") + 7
            end = assistant_text.find("```", start)
            assistant_text = assistant_text[start:end].strip()
        elif "```" in assistant_text:
            start = assistant_text.find("```") + 3
            end = assistant_text.find("```", start)
            assistant_text = assistant_text[start:end].strip()
        
        issues = json.loads(assistant_text)
        return issues
        
    except json.JSONDecodeError as e:
        return [{"category": "Error", "item": "Parse Error", "description": f"Could not parse response: {e}", "severity": "high"}]
    except Exception as e:
        return [{"category": "Error", "item": "API Error", "description": str(e), "severity": "high"}]

def require_api_key():
    """Check if OpenAI API key is configured, abort if not."""
    if not os.getenv("OPENAI_API_KEY"):
        abort(403, description="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")

@app.route('/')
def index():
    """Home page with upload form."""
    return render_template('index.html')

@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    """Handle URL analysis with direct CUA integration."""
    require_api_key()
    
    url = request.form.get('url')
    if not url:
        flash('Please provide a URL to analyze')
        return redirect(url_for('index'))
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        print(f"Analyzing URL: {url}")
        result = analyze_url_direct(url)
        
        if result["status"] == "error":
            flash(f'URL analysis failed: {result["error"]}')
            return redirect(url_for('index'))
        
        # Parse the response (expecting JSON format)
        issues = []
        try:
            if isinstance(result["data"], str):
                issues = json.loads(result["data"])
            elif isinstance(result["data"], list):
                issues = result["data"]
            else:
                issues = [{"category": "Analysis", "item": "AI Response", "description": str(result["data"]), "severity": "medium"}]
        except json.JSONDecodeError:
            # If not JSON, treat as plain text response
            issues = [{"category": "Analysis", "item": "AI Response", "description": result["data"], "severity": "medium"}]
        
        # Calculate summary stats
        total_issues = len(issues)
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        issues_by_category = {}
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            category = issue.get("category", "Other")
            
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            if category not in issues_by_category:
                issues_by_category[category] = []
            issues_by_category[category].append(issue)
        
        return render_template('report.html',
                             issues=issues,
                             issues_by_category=issues_by_category,
                             total_issues=total_issues,
                             severity_counts=severity_counts,
                             source=url,
                             source_type='url',
                             filename=url,
                             timestamp=datetime.now().strftime('%Y-%m-%d at %I:%M %p'))
        
    except Exception as e:
        flash(f'URL analysis failed: {str(e)}')
        return redirect(url_for('index'))

@app.route('/analyze/task', methods=['POST'])
def analyze_task():
    """Handle task-based URL analysis with interactive testing."""
    require_api_key()
    
    url = request.form.get('url')
    scenario = request.form.get('scenario')
    
    if not url:
        flash('Please provide a URL to analyze')
        return redirect(url_for('index'))
    
    if not scenario:
        flash('Please provide a scenario to test')
        return redirect(url_for('index'))
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        print(f"🎯 Interactive scenario testing: {scenario}")
        print(f"🌐 Target URL: {url}")
        
        # Use interactive agent for scenario testing
        result = analyze_url_direct(url, task=scenario)
        
        if result["status"] == "error":
            flash(f'Scenario testing failed: {result["error"]}')
            return redirect(url_for('index'))
        
        # Parse the response (expecting list of issues from interactive analysis)
        issues = []
        if result["status"] == "success" and result.get("data"):
            if isinstance(result["data"], list):
                issues = result["data"]
            elif isinstance(result["data"], str):
                # Try to parse as JSON
                try:
                    issues = json.loads(result["data"])
                except json.JSONDecodeError:
                    # If not JSON, create a single issue with the text
                    issues = [{
                        "category": "Interactive Analysis",
                        "item": "Scenario Testing Results",
                        "description": result["data"],
                        "severity": "medium",
                        "scenario_impact": "Overall results from interactive testing"
                    }]
            else:
                issues = [{
                    "category": "Interactive Analysis",
                    "item": "Scenario Testing",
                    "description": str(result["data"]),
                    "severity": "medium",
                    "scenario_impact": "Analysis results"
                }]
        
        # If no issues found, add a placeholder
        if not issues:
            issues = [{
                "category": "Interactive Analysis",
                "item": "Scenario Completion",
                "description": "Interactive testing completed. Check server logs for detailed action history.",
                "severity": "low",
                "scenario_impact": "Testing session completed successfully"
            }]
        
        # Calculate summary stats
        total_issues = len(issues)
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        issues_by_category = {}
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            category = issue.get("category", "Other")
            
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            if category not in issues_by_category:
                issues_by_category[category] = []
            issues_by_category[category].append(issue)
        
        return render_template('report.html',
                             issues=issues,
                             issues_by_category=issues_by_category,
                             total_issues=total_issues,
                             severity_counts=severity_counts,
                             source=f"{url} (Interactive Scenario: {scenario})",
                             source_type='interactive_task',
                             filename=url,
                             scenario=scenario,
                             timestamp=datetime.now().strftime('%Y-%m-%d at %I:%M %p'))
        
    except Exception as e:
        print(f"❌ Interactive testing failed: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Interactive scenario testing failed: {str(e)}')
        return redirect(url_for('index'))

@app.route('/analyze/upload', methods=['POST'])
def analyze_upload():
    """Handle file upload analysis with direct CUA integration."""
    require_api_key()
    
    if 'screenshot' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['screenshot']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"Analyzing file: {filepath}")
        result = analyze_upload_direct(filepath)
        
        if result["status"] == "error":
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            flash(f'File analysis failed: {result["error"]}')
            return redirect(url_for('index'))
        
        # Parse the response (expecting JSON format)
        issues = []
        try:
            if isinstance(result["data"], str):
                issues = json.loads(result["data"])
            elif isinstance(result["data"], list):
                issues = result["data"]
            else:
                issues = [{"category": "Analysis", "item": "AI Response", "description": str(result["data"]), "severity": "medium"}]
        except json.JSONDecodeError:
            # If not JSON, treat as plain text response
            issues = [{"category": "Analysis", "item": "AI Response", "description": result["data"], "severity": "medium"}]
        
        # Calculate summary stats
        total_issues = len(issues)
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        issues_by_category = {}
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            category = issue.get("category", "Other")
            
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            if category not in issues_by_category:
                issues_by_category[category] = []
            issues_by_category[category].append(issue)
        
        # Encode image for display
        with open(filepath, "rb") as img:
            img_b64 = base64.b64encode(img.read()).decode()
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return render_template('report.html',
                             issues=issues,
                             issues_by_category=issues_by_category,
                             total_issues=total_issues,
                             severity_counts=severity_counts,
                             source=file.filename,
                             source_type='file',
                             image_data=img_b64,
                             filename=file.filename,
                             timestamp=datetime.now().strftime('%Y-%m-%d at %I:%M %p'))
        
    except Exception as e:
        # Clean up file on error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        flash(f'File analysis failed: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic analysis."""
    require_api_key()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        file.save(tmp_file.name)
        
        try:
            checklist = load_checklist()
            issues = analyze_screenshot_with_openai(tmp_file.name, checklist)
            
            # Calculate stats
            total_issues = len(issues)
            severity_counts = {"high": 0, "medium": 0, "low": 0}
            
            for issue in issues:
                severity = issue.get("severity", "medium")
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            return jsonify({
                'success': True,
                'issues': issues,
                'summary': {
                    'total_issues': total_issues,
                    'severity_counts': severity_counts
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up temp file
            os.unlink(tmp_file.name)

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

@app.route('/api/workflow', methods=['POST'])
def api_workflow():
    """API endpoint for enhanced workflow analysis with scenarios."""
    require_api_key()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    url = data.get('url')
    scenario = data.get('scenario', 'general analysis')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        print(f"🌐 Starting enhanced workflow analysis")
        print(f"📍 URL: {url}")
        print(f"🎯 Scenario: {scenario}")
        
        # Import and run the enhanced workflow
        from workflow import run_workflow
        import asyncio
        
        # Run the async workflow
        result = asyncio.run(run_workflow(url, scenario))
        
        print(f"✅ Workflow completed with status: {result.get('status', 'unknown')}")
        
        return jsonify({
            'success': True,
            'result': result,
            'url': url,
            'scenario': scenario,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        return jsonify({
            'error': str(e),
            'url': url,
            'scenario': scenario
        }), 500

if __name__ == '__main__':
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
    
    print("🚀 Starting UX Analyzer Web Application...")
    print("📍 Visit: http://127.0.0.1:5006")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(host="0.0.0.0", port=5006, debug=True)
