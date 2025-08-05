import os
import sys
import json
import base64
import openai
from datetime import datetime

# Load environment variables if not already set
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

# Load your checklist JSON
with open("uiux_checklist.json") as f:
    CHECKLIST = json.load(f)

def format_checklist(checklist):
    lines = []
    for category, items in checklist.items():
        lines.append(f"## {category}")
        for it in items:
            lines.append(f"- {it}")
    return "\n".join(lines)

def build_prompt():
    return f"""
You are a UX expert. Analyze the supplied screenshot using this checklist:
{format_checklist(CHECKLIST)}

Return a JSON array of issues, where each issue has:
- category: which checklist section
- item: the specific checklist item
- description: what's wrong
- severity: "high", "medium", or "low"
- (optional) bbox: [x, y, width, height]
Respond only with valid JSON.
"""

def analyze_screenshot_simple(screenshot_path: str):
    """Simple version using OpenAI's vision API directly."""
    client = openai.OpenAI()
    
    # Read and encode the screenshot
    with open(screenshot_path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": build_prompt()
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
        
        # Extract the response text
        assistant_text = response.choices[0].message.content
        
        # Try to parse as JSON, handling markdown code blocks
        try:
            # Remove markdown code blocks if present
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
            # If it's not valid JSON, wrap it in a simple structure
            return [{"category": "Analysis", "item": "Parse Error", "description": f"Could not parse JSON: {e}. Raw response: {assistant_text[:500]}...", "severity": "high"}]
            
    except Exception as e:
        return [{"category": "Error", "item": "API Call Failed", "description": str(e), "severity": "high"}]

def get_severity_color(severity):
    """Get color for severity level."""
    severity_colors = {
        "high": "#dc3545",    # Red
        "medium": "#fd7e14",  # Orange
        "low": "#28a745"      # Green
    }
    return severity_colors.get(severity.lower(), "#6c757d")  # Default gray

def get_severity_icon(severity):
    """Get icon for severity level."""
    severity_icons = {
        "high": "⚠️",
        "medium": "⚡",
        "low": "ℹ️"
    }
    return severity_icons.get(severity.lower(), "•")

def generate_html_report(issues, screenshot_path):
    """Generate an HTML report from the UX analysis results."""
    
    # Encode screenshot for embedding
    with open(screenshot_path, "rb") as img:
        screenshot_b64 = base64.b64encode(img.read()).decode()
    
    # Group issues by category
    issues_by_category = {}
    total_issues = len(issues)
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    
    for issue in issues:
        category = issue.get("category", "Other")
        severity = issue.get("severity", "medium")
        
        if category not in issues_by_category:
            issues_by_category[category] = []
        issues_by_category[category].append(issue)
        severity_counts[severity] += 1
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d at %I:%M %p")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UX Analysis Report - {os.path.basename(screenshot_path)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            color: #6c757d;
            font-size: 1.1em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .summary-card h3 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .summary-card.total {{ color: #2c3e50; }}
        .summary-card.high {{ color: #dc3545; }}
        .summary-card.medium {{ color: #fd7e14; }}
        .summary-card.low {{ color: #28a745; }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        
        .screenshot-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .screenshot-section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        .screenshot {{
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .issues-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .issues-section h2 {{
            color: #2c3e50;
            margin-bottom: 25px;
            font-size: 1.5em;
        }}
        
        .category {{
            margin-bottom: 30px;
        }}
        
        .category-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #007bff;
        }}
        
        .category-header h3 {{
            color: #2c3e50;
            font-size: 1.2em;
        }}
        
        .issue {{
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #dee2e6;
        }}
        
        .issue.high {{ border-left-color: #dc3545; }}
        .issue.medium {{ border-left-color: #fd7e14; }}
        .issue.low {{ border-left-color: #28a745; }}
        
        .issue-header {{
            display: flex;
            align-items: center;
            justify-content: between;
            margin-bottom: 10px;
        }}
        
        .issue-title {{
            font-weight: 600;
            color: #2c3e50;
            flex: 1;
        }}
        
        .severity-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            color: white;
            margin-left: 10px;
        }}
        
        .issue-description {{
            color: #6c757d;
            line-height: 1.6;
        }}
        
        .bbox {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #6c757d;
            background: #f8f9fa;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: monospace;
        }}
        
        @media (max-width: 768px) {{
            .content-grid {{
                grid-template-columns: 1fr;
            }}
            
            .summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 UX Analysis Report</h1>
            <div class="meta">
                <strong>File:</strong> {os.path.basename(screenshot_path)} • 
                <strong>Generated:</strong> {timestamp}
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>{total_issues}</h3>
                <p>Total Issues</p>
            </div>
            <div class="summary-card high">
                <h3>{severity_counts['high']}</h3>
                <p>High Priority</p>
            </div>
            <div class="summary-card medium">
                <h3>{severity_counts['medium']}</h3>
                <p>Medium Priority</p>
            </div>
            <div class="summary-card low">
                <h3>{severity_counts['low']}</h3>
                <p>Low Priority</p>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="screenshot-section">
                <h2>📸 Analyzed Screenshot</h2>
                <img src="data:image/png;base64,{screenshot_b64}" alt="Analyzed Screenshot" class="screenshot">
            </div>
            
            <div class="issues-section">
                <h2>📋 Issues Found</h2>
"""

    # Add issues by category
    for category, category_issues in issues_by_category.items():
        html_content += f"""
                <div class="category">
                    <div class="category-header">
                        <h3>{category} ({len(category_issues)} issues)</h3>
                    </div>
"""
        
        for issue in category_issues:
            severity = issue.get("severity", "medium")
            item = issue.get("item", "Unknown")
            description = issue.get("description", "No description provided")
            bbox = issue.get("bbox")
            
            bbox_html = ""
            if bbox:
                bbox_html = f'<div class="bbox">📍 Location: x:{bbox[0]}, y:{bbox[1]}, w:{bbox[2]}, h:{bbox[3]}</div>'
            
            html_content += f"""
                    <div class="issue {severity}">
                        <div class="issue-header">
                            <div class="issue-title">{get_severity_icon(severity)} {item}</div>
                            <div class="severity-badge" style="background-color: {get_severity_color(severity)}">{severity.upper()}</div>
                        </div>
                        <div class="issue-description">{description}</div>
                        {bbox_html}
                    </div>
"""
        
        html_content += "                </div>"

    html_content += """
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def analyze_screenshot(path: str):
    print("🔍 Analyzing screenshot...")
    issues = analyze_screenshot_simple(path)
    
    print("📄 Generating HTML report...")
    html_content = generate_html_report(issues, path)
    
    # Save HTML file
    report_filename = f"ux_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report saved as: {report_filename}")
    
    # Also output JSON for compatibility
    print("\n📊 JSON Results:")
    print(json.dumps(issues, indent=2))
    
    return report_filename

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ux_analyzer_html.py <screenshot.png>")
        sys.exit(1)
    
    report_file = analyze_screenshot(sys.argv[1])
    
    # Open in default browser
    import webbrowser
    import os
    full_path = os.path.abspath(report_file)
    webbrowser.open(f'file://{full_path}')
    print(f"🌐 Opening report in browser: {report_file}")
