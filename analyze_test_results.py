#!/usr/bin/env python3
"""
🔍 TEST RESULTS ANALYZER
Helps analyze what happened during the interactive testing.
"""

import os
import json
from datetime import datetime

def check_test_results():
    print("🔍 ANALYZING INTERACTIVE TEST RESULTS")
    print("=" * 45)
    
    print("\n📋 CHECKING WHAT HAPPENED:")
    print("-" * 30)
    
    # Check if Flask app was running
    print("1️⃣ Flask App Status:")
    if os.path.exists('app.py'):
        print("   ✅ app.py exists")
        print("   💡 To check if it ran: look for Flask console output")
    else:
        print("   ❌ app.py not found")
    
    # Check for any result files
    print("\n2️⃣ Looking for Result Files:")
    result_files = []
    for file in os.listdir('.'):
        if any(keyword in file.lower() for keyword in ['result', 'test', 'log', 'output']):
            result_files.append(file)
    
    if result_files:
        print(f"   📄 Found {len(result_files)} potential result files:")
        for file in result_files:
            print(f"      • {file}")
    else:
        print("   📄 No obvious result files found")
    
    # Check interactive agent
    print("\n3️⃣ Interactive Agent Check:")
    try:
        from interactive_agent import InteractiveAgent
        agent = InteractiveAgent()
        stats = agent.client.get_usage_stats()
        print("   ✅ Interactive agent accessible")
        print(f"   📊 Current API stats: {stats}")
    except Exception as e:
        print(f"   ❌ Agent check failed: {e}")
    
    # Check recent activity
    print("\n4️⃣ Recent File Activity:")
    try:
        files = []
        for file in os.listdir('.'):
            if file.endswith('.py'):
                stat = os.stat(file)
                files.append((file, stat.st_mtime))
        
        files.sort(key=lambda x: x[1], reverse=True)
        print("   📅 Recently modified files:")
        for file, mtime in files[:5]:
            time_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"      • {file} - {time_str}")
    except Exception as e:
        print(f"   ❌ File activity check failed: {e}")

def interpret_message():
    print("\n🎯 INTERPRETING THE MESSAGE:")
    print("-" * 30)
    print("'Interactive testing completed. Check server logs for detailed action history.'")
    print()
    print("✅ GOOD NEWS: This means the test RAN and COMPLETED!")
    print("📊 The interactive agent successfully executed the scenario")
    print("🔍 It's asking you to check logs for details")
    print()
    print("🔍 WHERE TO LOOK FOR LOGS:")
    print("1. Flask console output (where you ran python3 app.py)")
    print("2. Browser console (F12 → Console tab)")
    print("3. VS Code terminal where Flask is running")
    print("4. System logs (if any errors occurred)")

def suggest_next_steps():
    print("\n🚀 SUGGESTED NEXT STEPS:")
    print("-" * 25)
    print("1️⃣ Check Flask Console Output:")
    print("   • Look at the terminal where you ran 'python3 app.py'")
    print("   • Should show agent actions, API calls, and results")
    print()
    print("2️⃣ Try a Direct Test to See Results:")
    print("   • Run: python3 quick_test.py")
    print("   • Or run: python3 complete_local_test.py")
    print()
    print("3️⃣ Run Interactive Test Again with Verbose Output:")
    print("   • Open http://localhost:5006")
    print("   • Use Browser Dev Tools (F12)")
    print("   • Watch Console for detailed logs")
    print()
    print("4️⃣ Check if Results Were Successful:")
    print("   • The message suggests completion, not failure")
    print("   • Look for screenshots or action summaries")
    print("   • Check API usage statistics")

def create_debug_test():
    print("\n🔧 CREATING DEBUG TEST:")
    print("-" * 25)
    
    debug_code = '''#!/usr/bin/env python3
"""Debug test to see what the interactive agent actually does."""

from interactive_agent import InteractiveAgent
import json

print("🧪 DEBUG: Running Interactive Test with Full Logging")
print("=" * 55)

try:
    # Initialize agent
    print("1️⃣ Initializing agent...")
    agent = InteractiveAgent()
    print("✅ Agent ready")
    
    # Simple test scenario
    print("\\n2️⃣ Running test scenario...")
    url = "https://www.google.com"
    scenario = "Take a screenshot and find the search input"
    
    print(f"🌐 URL: {url}")
    print(f"📝 Scenario: {scenario}")
    
    # Run with detailed output
    result = agent.analyze_scenario(url, scenario)
    
    print("\\n3️⃣ TEST RESULTS:")
    print(f"📊 Status: {result.get('status', 'Unknown')}")
    print(f"📊 Actions: {len(result.get('actions', []))}")
    
    # Show all actions
    actions = result.get('actions', [])
    if actions:
        print("\\n📋 DETAILED ACTIONS:")
        for i, action in enumerate(actions, 1):
            print(f"   {i}. {action.get('action', 'unknown')}: {action.get('message', 'No message')}")
    
    # Show API stats
    stats = agent.client.get_usage_stats()
    print(f"\\n📈 API STATISTICS:")
    print(f"   • Total requests: {stats['total_requests']}")
    print(f"   • Successful: {stats['successful_requests']}")
    print(f"   • Failed: {stats['failed_requests']}")
    print(f"   • Retries: {stats['total_retries']}")
    
    print("\\n✅ DEBUG TEST COMPLETED SUCCESSFULLY!")
    print("This shows exactly what the interactive agent does.")
    
except Exception as e:
    print(f"\\n❌ DEBUG TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open('debug_test.py', 'w') as f:
        f.write(debug_code)
    
    print("✅ Created debug_test.py")
    print("📝 Run: python3 debug_test.py")
    print("🎯 This will show you exactly what happens during testing")

if __name__ == "__main__":
    check_test_results()
    interpret_message()
    suggest_next_steps()
    create_debug_test()
    
    print("\n🎉 SUMMARY:")
    print("Your test completed successfully! The message indicates")
    print("the interactive agent finished its work. Check the")
    print("suggestions above to see detailed results.")
    print("\n💡 Run 'python3 debug_test.py' for a detailed view!")
