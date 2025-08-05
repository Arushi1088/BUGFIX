#!/usr/bin/env python3

"""
🧪 STEP 1: Unit Test - Direct Agent Testing
Test the InteractiveUXAgent directly to verify end-to-end flow
"""

import sys
import os

# Add current directory to path
sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

def test_agent_directly():
    """Test the interactive agent with a simple HTML test page."""
    
    print("🧪 STEP 1: UNIT TEST - Direct Agent Testing")
    print("=" * 60)
    
    # Create a simple test HTML file
    test_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UX Test Page</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .contact-btn { 
            background: #007bff; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-size: 16px;
            margin: 20px 0;
        }
        .contact-btn:hover { background: #0056b3; }
        .content { max-width: 800px; }
        .hidden { display: none; }
        #contact-form { 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 5px; 
            margin-top: 20px;
        }
        input[type="text"], input[type="email"], textarea {
            width: 100%;
            padding: 8px;
            margin: 5px 0 15px 0;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Welcome to Our Test Website</h1>
        <p>This is a test page for UX analysis. We offer various services and would love to hear from you.</p>
        
        <button class="contact-btn" onclick="showContactForm()">Contact Us</button>
        
        <div id="contact-form" class="hidden">
            <h3>Contact Form</h3>
            <form>
                <label>Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label>Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label>Message:</label>
                <textarea id="message" name="message" rows="4" required></textarea>
                
                <button type="submit" class="contact-btn">Send Message</button>
            </form>
        </div>
        
        <div id="success-message" class="hidden" style="color: green; margin-top: 20px;">
            <h3>Thank you!</h3>
            <p>Your message has been received. We'll get back to you soon.</p>
        </div>
    </div>
    
    <script>
        function showContactForm() {
            document.getElementById('contact-form').classList.remove('hidden');
            document.querySelector('.contact-btn').style.display = 'none';
        }
        
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('contact-form').classList.add('hidden');
            document.getElementById('success-message').classList.remove('hidden');
        });
    </script>
</body>
</html>
"""
    
    # Write test HTML file
    test_file_path = "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/test_page.html"
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_html_content)
    
    print(f"✅ Created test HTML file: {test_file_path}")
    
    # Test the agent
    try:
        from interactive_agent import InteractiveUXAgent
        print("✅ InteractiveUXAgent imported successfully")
        
        agent = InteractiveUXAgent()
        print("✅ Agent created")
        
        # Use file:// URL for local testing
        test_url = f"file://{test_file_path}"
        test_scenario = "Click the Contact Us button and verify the form appears"
        
        print(f"\\n🎯 Testing scenario: {test_scenario}")
        print(f"🌐 Test URL: {test_url}")
        
        result = agent.analyze_scenario(test_url, test_scenario)
        
        # Verify the result structure
        print("\\n📊 RESULT VERIFICATION:")
        print("=" * 40)
        
        assert "status" in result, "Result missing 'status' field"
        print(f"✅ Status: {result['status']}")
        
        assert result["status"] == "success", f"Expected success, got: {result['status']}"
        print("✅ Status is 'success'")
        
        assert "final_analysis" in result, "Result missing 'final_analysis' field"
        print("✅ Contains 'final_analysis' field")
        
        final_analysis = result["final_analysis"]
        assert "issues" in final_analysis, "final_analysis missing 'issues' field"
        print("✅ Contains 'issues' in final_analysis")
        
        issues = final_analysis["issues"]
        print(f"✅ Issues found: {len(issues)}")
        
        # Print detailed results
        print("\\n📋 DETAILED RESULTS:")
        print("=" * 40)
        
        print(f"Actions taken: {result.get('action_count', 0)}")
        print(f"Conversation turns: {result.get('conversation_turns', 0)}")
        
        if issues:
            print("\\n🔍 Issues identified:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. [{issue.get('severity', 'unknown')}] {issue.get('category', 'Unknown')}")
                print(f"      {issue.get('item', 'No title')}")
                print(f"      {issue.get('description', 'No description')[:100]}...")
        else:
            print("ℹ️  No issues found in final analysis")
        
        print("\\n🎯 UNIT TEST RESULT: ✅ PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Unit test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent_directly()
    if success:
        print("\\n🌟 Step 1 completed successfully - Agent works end-to-end!")
    else:
        print("\\n💥 Step 1 failed - Issues with agent flow")
        sys.exit(1)
