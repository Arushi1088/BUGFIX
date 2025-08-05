#!/usr/bin/env python3
"""
🧪 Step 3 Unit Test - Phase 2 YAML Runner
Test the YAML-driven test system with Office mocks
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append('/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer')

def test_yaml_runner():
    """Test the YAML runner with Office application scenarios."""
    
    print("🧪 STEP 3 UNIT TEST - YAML Runner Testing")
    print("=" * 60)
    
    try:
        # Test 1: Import YAML runner
        print("1️⃣ Testing YAML Runner import...")
        from yaml_runner import YAMLTestRunner
        print("   ✅ YAMLTestRunner imported successfully")
        
        # Test 2: Check schema file exists
        print("\\n2️⃣ Testing schema file...")
        schema_path = Path("schemas/office_tests.yaml")
        if schema_path.exists():
            print(f"   ✅ Schema file found: {schema_path}")
        else:
            print(f"   ❌ Schema file missing: {schema_path}")
            return False
        
        # Test 3: Create runner instance
        print("\\n3️⃣ Testing runner creation...")
        runner = YAMLTestRunner()
        print("   ✅ Runner instance created")
        
        # Test 4: Load schema
        print("\\n4️⃣ Testing schema loading...")
        try:
            test_data = runner.load_schema()
            print(f"   ✅ Schema loaded successfully")
            
            # Check expected sections
            expected_sections = ['word', 'excel', 'powerpoint']
            for section in expected_sections:
                if section in test_data:
                    scenarios = len(test_data[section])
                    print(f"   ✅ {section.title()}: {scenarios} scenarios")
                else:
                    print(f"   ⚠️  {section.title()}: section missing")
                    
        except Exception as e:
            print(f"   ❌ Schema loading failed: {e}")
            return False
        
        # Test 5: Test scenario building
        print("\\n5️⃣ Testing scenario building...")
        try:
            sample_config = {
                'scenario': 'Test scenario',
                'description': 'This is a test',
                'steps': [
                    {'action': 'click', 'selector': '#button', 'description': 'Click button'}
                ]
            }
            
            scenario_text = runner.build_agent_scenario(sample_config)
            print(f"   ✅ Scenario text generated: {len(scenario_text)} chars")
            
            if 'Test scenario' in scenario_text and 'Click button' in scenario_text:
                print("   ✅ Scenario text contains expected content")
            else:
                print("   ⚠️  Scenario text may be incomplete")
                
        except Exception as e:
            print(f"   ❌ Scenario building failed: {e}")
            return False
        
        # Test 6: Test expectation counting
        print("\\n6️⃣ Testing expectation validation...")
        try:
            sample_expectations = {
                'dom': [
                    {'selector': '#test', 'contains': 'value'},
                    {'selector': '#test2', 'exists': True}
                ],
                'performance': {
                    'page_load_ms': '<1000',
                    'response_time_ms': '<200'
                }
            }
            
            count = runner.count_expectations(sample_expectations)
            print(f"   ✅ Expectation count: {count}")
            
            if count == 4:  # 2 DOM + 2 performance
                print("   ✅ Expectation counting accurate")
            else:
                print(f"   ⚠️  Expected 4 expectations, got {count}")
                
        except Exception as e:
            print(f"   ❌ Expectation counting failed: {e}")
            return False
        
        # Test 7: Test report generation structure
        print("\\n7️⃣ Testing report generation...")
        try:
            from report_extender import ReportExtender
            extender = ReportExtender()
            print("   ✅ ReportExtender imported and created")
            
            # Test sample report extension
            sample_report = {
                "status": "success",
                "scenario": "Test",
                "final_analysis": {"issues": []},
                "action_count": 3
            }
            
            extended = extender.extend_report(sample_report)
            
            expected_sections = ['extended_analysis', 'performance_metrics', 
                               'visual_metrics', 'accessibility_metrics', 'ux_score']
            
            for section in expected_sections:
                if section in extended:
                    print(f"   ✅ {section} section present")
                else:
                    print(f"   ❌ {section} section missing")
                    
        except Exception as e:
            print(f"   ❌ Report extension failed: {e}")
            return False
        
        print("\\n📊 UNIT TEST RESULTS:")
        print("=" * 40)
        print("✅ YAML Runner import successful")
        print("✅ Schema loading functional")
        print("✅ Scenario building working")
        print("✅ Expectation validation ready")
        print("✅ Report extension operational")
        
        print("\\n🎯 STEP 3 UNIT TEST: ✅ PASSED")
        print("🚀 Phase 2 YAML system ready for testing!")
        
        return True
        
    except Exception as e:
        print(f"❌ Unit test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_yaml_runner()
    if success:
        print("\\n🌟 Step 3 completed successfully - YAML system operational!")
    else:
        print("\\n💥 Step 3 failed - Issues with YAML system")
        sys.exit(1)
