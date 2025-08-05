#!/usr/bin/env python3
"""
🚀 UX Analyzer Startup Script
Properly starts the Flask web application with all dependencies.
"""

import os
import sys

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"🔑 OpenAI API key: {'*' * 10 + api_key[-4:] if len(api_key) > 4 else 'Set'}")
    else:
        print("⚠️  OpenAI API key not found!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # Check required modules
    required_modules = ['flask', 'openai', 'playwright', 'python-dotenv']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module} - installed")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} - missing")
    
    if missing_modules:
        print(f"\n📦 Install missing modules with:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False
    
    return True

def start_app():
    """Start the Flask application."""
    if not check_environment():
        print("\n❌ Environment check failed. Fix issues above before starting.")
        return
    
    print("\n🚀 Starting UX Analyzer Web Application...")
    print("📍 The app will be available at: http://127.0.0.1:5006")
    print("📍 Or try: http://localhost:5006")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(host="127.0.0.1", port=5006, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running directly with: python3 app.py")

if __name__ == "__main__":
    start_app()
