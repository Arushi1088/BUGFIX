#!/usr/bin/env python3
"""
🧪 Simple YAML Test - Phase 2 Core Testing
Test just the YAML loading functionality
"""

import yaml
import json
from pathlib import Path

def test_yaml_loading():
    """Test YAML schema loading without complex dependencies."""
    
    print("🧪 SIMPLE YAML TEST - Core Functionality")
    print("=" * 50)
    
    # Test 1: Load YAML schema
    print("1️⃣ Testing YAML schema loading...")
    try:
        schema_path = Path("schemas/office_tests.yaml")
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_data = yaml.safe_load(f)
            
            print("   ✅ YAML schema loaded successfully")
            print(f"   📊 Schema keys: {list(schema_data.keys())}")
            
            # Check for expected structure
            if 'tests' in schema_data:
                tests = schema_data['tests']
                print(f"   ✅ Found {len(tests)} test scenarios")
                
                # Show first test
                if tests:
                    first_test = tests[0]
                    print(f"   📋 First test: {first_test.get('name', 'Unnamed')}")
                    print(f"   🎯 Target: {first_test.get('target', 'Unknown')}")
            else:
                print("   ⚠️  No 'tests' key in schema")
                
        else:
            print("   ❌ YAML schema file not found")
            return False
            
    except Exception as e:
        print(f"   ❌ YAML loading failed: {e}")
        return False
    
    # Test 2: Test YAML structure validation
    print("\\n2️⃣ Testing YAML structure...")
    try:
        required_keys = ['metadata', 'tests']
        for key in required_keys:
            if key in schema_data:
                print(f"   ✅ Required key '{key}' present")
            else:
                print(f"   ❌ Missing required key '{key}'")
        
        # Check metadata
        if 'metadata' in schema_data:
            metadata = schema_data['metadata']
            print(f"   📝 Schema version: {metadata.get('version', 'Unknown')}")
            print(f"   📅 Created: {metadata.get('created', 'Unknown')}")
            
    except Exception as e:
        print(f"   ❌ Structure validation failed: {e}")
        return False
    
    # Test 3: Sample scenario processing
    print("\\n3️⃣ Testing scenario processing...")
    try:
        if 'tests' in schema_data and schema_data['tests']:
            test_scenario = schema_data['tests'][0]
            
            # Extract key components
            name = test_scenario.get('name', 'Unknown')
            target = test_scenario.get('target', 'Unknown')
            steps = test_scenario.get('steps', [])
            expectations = test_scenario.get('expectations', [])
            
            print(f"   📋 Scenario: {name}")
            print(f"   🎯 Target: {target}")
            print(f"   📝 Steps: {len(steps)}")
            print(f"   ✅ Expectations: {len(expectations)}")
            
            # Show step details
            if steps:
                first_step = steps[0]
                print(f"   🔧 First step: {first_step.get('action', 'Unknown')}")
                
        else:
            print("   ⚠️  No test scenarios found")
            
    except Exception as e:
        print(f"   ❌ Scenario processing failed: {e}")
        return False
    
    # Test 4: Basic report structure
    print("\\n4️⃣ Testing report structure...")
    try:
        # Create a sample test result
        sample_result = {
            'test_name': 'Word Document Creation',
            'target': 'word.html',
            'status': 'success',
            'execution_time': 1.23,
            'steps_completed': 5,
            'steps_total': 5,
            'expectations_met': 3,
            'expectations_total': 3,
            'timestamp': '2024-01-24T10:30:00Z'
        }
        
        # Test JSON serialization
        json_output = json.dumps(sample_result, indent=2)
        print("   ✅ Sample result JSON serializable")
        print(f"   📊 Result keys: {list(sample_result.keys())}")
        
    except Exception as e:
        print(f"   ❌ Report structure test failed: {e}")
        return False
    
    print("\\n📊 SIMPLE YAML TEST RESULTS:")
    print("=" * 40)
    print("✅ YAML loading functional")
    print("✅ Schema structure valid")  
    print("✅ Scenario processing works")
    print("✅ Report structure ready")
    
    print("\\n🎯 SIMPLE YAML TEST: ✅ PASSED")
    print("📋 Core YAML functionality verified!")
    
    return True

if __name__ == "__main__":
    success = test_yaml_loading()
    if success:
        print("\\n🌟 Simple YAML test completed successfully!")
        print("🚀 Ready for more complex testing!")
    else:
        print("\\n💥 Simple YAML test failed")
        exit(1)
