#!/usr/bin/env python3
"""
🖥️ UX Analyzer - CLI Interface
Command-line interface for the UX analyzer using the sample CUA CLI pattern.
"""

import os, sys
import unicodedata

# Force Python UTF8 mode if not already set
os.environ.setdefault("PYTHONUTF8", "1")

# Reconfigure stdout/stderr to UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv()   # pulls in .env into os.environ

import json
import argparse
from pathlib import Path
from datetime import datetime

# Import the existing analyzer functions
try:
    from ux_analyzer_simple import analyze_screenshot_simple, format_checklist
except ImportError:
    print("❌ Error: ux_analyzer_simple.py not found")
    print("   Make sure you're in the correct directory with the analyzer files")
    sys.exit(1)

def sanitize_prompt(raw_prompt):
    """Sanitize prompt to prevent Unicode encoding issues."""
    # 1) Normalize Unicode (NFKC turns fancy dashes into normal ones, etc.)
    norm = unicodedata.normalize("NFKC", raw_prompt)
    
    # 2) Strip any remaining non-ASCII by replacing them
    ascii_only = norm.encode("ascii", errors="ignore").decode("ascii")
    
    # 3) Return the cleaned up prompt
    return ascii_only

def load_checklist():
    """Load the UX checklist from JSON file."""
    try:
        with open('uiux_checklist.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: uiux_checklist.json not found")
        print("   Make sure the checklist file exists in the current directory")
        sys.exit(1)

def format_checklist(checklist):
    """Format checklist for prompt."""
    lines = []
    for category, items in checklist.items():
        lines.append(f"## {category}")
        for item in items:
            lines.append(f"- {item}")
    return "\n".join(lines)

def build_prompt():
    """Build the analysis prompt using the checklist."""
    checklist = load_checklist()
    raw_prompt = f"""
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
    return sanitize_prompt(raw_prompt)

def analyze_with_cli(image_path, output_format='json', output_file=None, custom_prompt=None):
    """Analyze screenshot using CLI interface."""
    
    # Validate input file
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return False
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print(f"🔍 Analyzing: {image_path}")
    
    try:
        # Perform analysis with custom prompt if provided
        issues = analyze_screenshot_simple(image_path, custom_prompt)
        
        # Calculate summary statistics
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
        
        # Prepare output
        result = {
            "analysis": {
                "image_path": image_path,
                "total_issues": total_issues,
                "severity_counts": severity_counts,
                "issues_by_category": len(issues_by_category),
                "timestamp": datetime.now().isoformat()
            },
            "issues": issues,
            "summary": {
                "categories": list(issues_by_category.keys()),
                "severity_breakdown": severity_counts
            }
        }
        
        # Output results
        if output_format.lower() == 'json':
            output_text = json.dumps(result, indent=2)
        elif output_format.lower() == 'summary':
            output_text = generate_summary_text(result)
        else:
            output_text = json.dumps(result, indent=2)
        
        # Write to file or stdout
        if output_file:
            with open(output_file, 'w') as f:
                f.write(output_text)
            print(f"✅ Results saved to: {output_file}")
        else:
            print("📊 Analysis Results:")
            print("-" * 50)
            print(output_text)
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return False

def generate_summary_text(result):
    """Generate a human-readable summary."""
    analysis = result["analysis"]
    issues = result["issues"]
    
    summary = []
    summary.append(f"🔍 UX Analysis Summary")
    summary.append(f"=" * 50)
    summary.append(f"📁 File: {analysis['image_path']}")
    summary.append(f"📊 Total Issues: {analysis['total_issues']}")
    summary.append(f"🔴 High Priority: {analysis['severity_counts']['high']}")
    summary.append(f"🟠 Medium Priority: {analysis['severity_counts']['medium']}")
    summary.append(f"🟡 Low Priority: {analysis['severity_counts']['low']}")
    summary.append("")
    
    # Group issues by category
    issues_by_category = {}
    for issue in issues:
        category = issue.get("category", "Other")
        if category not in issues_by_category:
            issues_by_category[category] = []
        issues_by_category[category].append(issue)
    
    summary.append("📋 Issues by Category:")
    summary.append("-" * 30)
    
    for category, category_issues in issues_by_category.items():
        summary.append(f"\n🏷️  {category} ({len(category_issues)} issues):")
        for i, issue in enumerate(category_issues, 1):
            severity_icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(issue.get("severity", "medium"), "⚪")
            summary.append(f"   {i}. {severity_icon} {issue.get('item', 'Unknown')}")
            summary.append(f"      {issue.get('description', 'No description')}")
    
    return "\n".join(summary)

def analyze_url_with_playwright(url, prompt):
    """Analyze a URL using Playwright automation."""
    try:
        from computers.default.local_playwright import LocalPlaywrightBrowser
        from agent.agent import Agent
        
        with LocalPlaywrightBrowser() as computer:
            agent = Agent(model="computer-use-preview", computer=computer, tools=[])
            
            # Navigate to the URL and take screenshot using proper computer methods
            computer.goto(url)
            screenshot_path = f"temp_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_b64 = computer.screenshot()
            
            # Save the base64 screenshot to a file
            import base64
            with open(screenshot_path, 'wb') as f:
                f.write(base64.b64decode(screenshot_b64))
            
            # Analyze the screenshot
            issues = analyze_screenshot_simple(screenshot_path, prompt)
            
            # Clean up temporary screenshot
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            
            return issues
            
    except Exception as e:
        print(f"❌ URL analysis failed: {str(e)}")
        return [{"category": "Error", "item": "URL Analysis Failed", "description": str(e), "severity": "high"}]

def main():
    """CLI main function."""
    parser = argparse.ArgumentParser(
        description="🔍 UX Analyzer - Analyze UI/UX screenshots or URLs using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ux_cli.py screenshot.png                                    # Analyze screenshot
  python ux_cli.py --url https://example.com                         # Analyze URL
  python ux_cli.py screenshot.png --format summary                   # Human-readable summary
  python ux_cli.py --url https://example.com --json                  # JSON output for URL
  python ux_cli.py screenshot.png -o report.json                     # Save to file
        """
    )
    
    # Input options
    parser.add_argument('image', nargs='?', help='Path to the screenshot image to analyze')
    parser.add_argument('--url', help='URL to analyze (alternative to image file)')
    parser.add_argument('--initial-screenshot', help='Path to initial screenshot file')
    
    # Output options
    parser.add_argument('--format', '-f', choices=['json', 'summary'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--json', action='store_const', const='json', dest='format',
                       help='Output in JSON format')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    
    # Agent options (for compatibility with the Flask integration)
    parser.add_argument('--computer', default='local-playwright', help='Computer type to use')
    parser.add_argument('--model', default='computer-use-preview', help='Model to use')
    parser.add_argument('--prompt', help='Custom prompt to use (overrides default)')
    
    parser.add_argument('--version', action='version', version='UX Analyzer CLI v1.0')
    
    args = parser.parse_args()
    
    # Print header
    print("🔍 UX Analyzer - CLI Interface", file=sys.stderr)
    print("=" * 40, file=sys.stderr)
    
    # Determine input source
    image_path = None
    if args.url:
        print(f"🌐 Analyzing URL: {args.url}", file=sys.stderr)
        # Use custom prompt if provided, otherwise build default - sanitize either way
        prompt = sanitize_prompt(args.prompt) if args.prompt else build_prompt()
        try:
            issues = analyze_url_with_playwright(args.url, prompt)
        except Exception as e:
            print(f"❌ URL analysis failed: {str(e)}", file=sys.stderr)
            sys.exit(1)
    elif args.initial_screenshot:
        image_path = args.initial_screenshot
    elif args.image:
        image_path = args.image
    else:
        print("❌ Error: Must provide either an image file or --url", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Analyze file if we have an image path
    if image_path:
        # Use custom prompt if provided, otherwise use default - sanitize either way
        prompt = sanitize_prompt(args.prompt) if args.prompt else None
        success = analyze_with_cli(image_path, args.format, args.output, prompt)
        if success:
            print("✅ Analysis completed successfully!", file=sys.stderr)
            sys.exit(0)
        else:
            print("❌ Analysis failed!", file=sys.stderr)
            sys.exit(1)
    else:
        # Handle URL analysis results
        total_issues = len(issues)
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        result = {
            "analysis": {
                "url": args.url,
                "total_issues": total_issues,
                "severity_counts": severity_counts,
                "timestamp": datetime.now().isoformat()
            },
            "issues": issues,
            "summary": {
                "severity_breakdown": severity_counts
            }
        }
        
        # Output results
        if args.format.lower() == 'json':
            output_text = json.dumps(result, indent=2)
        elif args.format.lower() == 'summary':
            output_text = generate_summary_text(result)
        else:
            output_text = json.dumps(result, indent=2)
        
        # Write to file or stdout
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)
            print(f"✅ Results saved to: {args.output}", file=sys.stderr)
        else:
            print(output_text)  # Output to stdout for subprocess capture
        
        print("✅ Analysis completed successfully!", file=sys.stderr)

if __name__ == '__main__':
    main()
