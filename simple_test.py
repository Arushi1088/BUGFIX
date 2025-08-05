#!/usr/bin/env python3
import sys
sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

try:
    print("Testing imports...")
    from interactive_agent import InteractiveAgent
    print("✅ InteractiveAgent imported successfully")
    
    agent = InteractiveAgent()
    print("✅ Agent initialized successfully")
    
    # Test batching suggestions
    scenario = "find the search button and click it"
    suggestions = agent._suggest_batch_optimizations(scenario)
    print(f"✅ Batching suggestions: {suggestions}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
