#!/usr/bin/env python3
"""
🧪 Test the simplified workflow system
"""

import os
from workflow import analyze_website_workflow, batch_analyze_workflow, cleanup_browser

def test_simple_workflow():
    """Test the basic workflow functionality."""
    print("🧪 Testing Simple Workflow System...")
    
    # Test URL analysis workflow
    test_url = "https://example.com"
    print(f"\n🎯 Testing single URL analysis: {test_url}")
    
    try:
        result = analyze_website_workflow(test_url)
        print(f"✅ Single URL test completed")
        print(f"   Status: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'success':
            print(f"   Data length: {len(result.get('data', ''))} characters")
            print(f"   Screenshot available: {'screenshot' in result}")
        elif result.get('status') == 'error':
            print(f"   Error: {result.get('error', 'unknown')}")
            
    except Exception as e:
        print(f"❌ Single URL test failed: {e}")
    
    # Test batch analysis (smaller batch for demo)
    test_urls = ["https://example.com", "https://httpbin.org"]
    print(f"\n🎯 Testing batch analysis: {len(test_urls)} URLs")
    
    try:
        batch_result = batch_analyze_workflow(test_urls)
        print(f"✅ Batch test completed")
        print(f"   Analyzed: {len(batch_result)} websites")
        
        for i, item in enumerate(batch_result):
            status = item['result'].get('status', 'unknown')
            print(f"   {i+1}. {item['url']}: {status}")
            
    except Exception as e:
        print(f"❌ Batch test failed: {e}")
    
    # Cleanup
    try:
        cleanup_browser()
        print("✅ Cleanup completed")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

if __name__ == "__main__":
    test_simple_workflow()
