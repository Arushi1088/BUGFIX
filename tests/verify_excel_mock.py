#!/usr/bin/env python3
"""
🧪 Excel Mock Verification - End-to-End Test
Verify InteractiveUXAgent can drive the Excel mock
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from interactive_agent import InteractiveUXAgent

def test_excel_mock():
    """Test InteractiveUXAgent with Excel mock."""
    
    print("🧪 EXCEL MOCK END-TO-END TEST")
    print("=" * 50)
    
    try:
        print("1️⃣ Initializing InteractiveUXAgent...")
        agent = InteractiveUXAgent()
        print("   ✅ Agent initialized successfully")
        
        print("\\n2️⃣ Testing Excel mock interaction...")
        
        # Test scenario: Enter values in cells A1 and B1
        result = agent.analyze_scenario(
            url="http://localhost:8000/mocks/excel.html",
            scenario="Enter values in cells A1 and B1, then calculate sum"
        )
        
        print(f"\\n📊 STATUS: {result.get('status', 'unknown')}")
        
        print("\\n🔧 ACTIONS TAKEN:")
        actions = result.get("actions_taken", [])
        if actions:
            for i, action in enumerate(actions, 1):
                success_icon = "✅" if action.get("success", False) else "❌"
                action_type = action.get("action", "unknown")
                details = action.get("details", "")
                print(f"   {i}. {action_type} → {success_icon}")
                if details:
                    print(f"      Details: {details}")
        else:
            print("   ⚠️  No actions recorded")
        
        print("\\n📋 FINAL ANALYSIS:")
        final_analysis = result.get("final_analysis", {})
        if isinstance(final_analysis, dict):
            summary = final_analysis.get("summary", "No summary available")
            print(f"   {summary}")
            
            # Check for specific Excel mock elements
            if "elements" in final_analysis:
                elements = final_analysis["elements"]
                print(f"   🔍 Elements found: {len(elements)}")
                
                # Look for Excel-specific elements
                excel_elements = ["grid", "formula-bar", "new-sheet", "sum", "cell"]
                found_elements = []
                for elem in excel_elements:
                    if any(elem in str(e).lower() for e in elements):
                        found_elements.append(elem)
                
                if found_elements:
                    print(f"   📊 Excel elements detected: {', '.join(found_elements)}")
                else:
                    print("   ⚠️  No Excel-specific elements detected")
        else:
            print(f"   {final_analysis}")
        
        # Check if the test was successful
        status = result.get("status", "").lower()
        if status == "success":
            print("\\n🎉 EXCEL MOCK TEST: ✅ PASSED")
            print("🌟 InteractiveUXAgent successfully drove the Excel mock!")
            return True
        else:
            print("\\n💥 EXCEL MOCK TEST: ❌ FAILED")
            print(f"🚨 Status: {status}")
            return False
            
    except Exception as e:
        print(f"\\n💥 EXCEL MOCK TEST: ❌ EXCEPTION")
        print(f"🚨 Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🌐 Testing Excel Mock at: http://localhost:8000/mocks/excel.html")
    print("🤖 Using InteractiveUXAgent for automation")
    print("\\nStarting test...")
    
    success = test_excel_mock()
    
    if success:
        print("\\n🚀 Excel mock verification completed successfully!")
    else:
        print("\\n🛠️  Excel mock verification failed - check agent setup")
        sys.exit(1)
