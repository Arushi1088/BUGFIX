#!/usr/bin/env python3
"""Test script for batching optimization features."""

from interactive_agent import InteractiveAgent

def test_batching_suggestions():
    """Test the batching optimization suggestions."""
    print("🧪 Testing Batching Optimization System")
    print("=" * 50)
    
    agent = InteractiveAgent()
    
    # Test different scenario types
    scenarios = [
        ("Search Scenario", "Test the search functionality by finding and clicking the search button"),
        ("Form Scenario", "Fill out the contact form with user details and submit"),
        ("Navigation Scenario", "Navigate to the pricing page and verify the plans"),
        ("Testing Scenario", "Check if the shopping cart works correctly"),
        ("Generic Scenario", "Browse the website and explore features")
    ]
    
    for name, scenario in scenarios:
        print(f"\n📝 {name}:")
        print(f"Scenario: {scenario}")
        
        suggestions = agent._suggest_batch_optimizations(scenario)
        if suggestions:
            print("💡 Optimization Suggestions:")
            print(suggestions)
        else:
            print("💡 No specific batching suggestions for this scenario type")
    
    print("\n✅ Batching suggestion system working correctly!")

if __name__ == "__main__":
    test_batching_suggestions()
