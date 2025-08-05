#!/usr/bin/env python3
"""
🎯 Phase 2 Status Check - Quick Verification
Verify all Phase 2 components are working
"""

import yaml
import json
import requests
import os
from pathlib import Path

def check_phase2_status():
    """Quick verification of Phase 2 components."""
    
    print("🎯 PHASE 2 STATUS CHECK")
    print("=" * 50)
    
    status = {
        'yaml_system': False,
        'office_mocks': False,
        'server_running': False,
        'schemas_valid': False
    }
    
    # 1. Check YAML System
    print("1️⃣ Checking YAML system...")
    try:
        import yaml
        schema_path = Path("schemas/office_tests.yaml")
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_data = yaml.safe_load(f)
            if 'tests' in schema_data:
                status['yaml_system'] = True
                print("   ✅ YAML system operational")
            else:
                print("   ⚠️  YAML schema missing tests")
        else:
            print("   ❌ YAML schema file not found")
    except Exception as e:
        print(f"   ❌ YAML system error: {e}")
    
    # 2. Check Office Mocks
    print("\\n2️⃣ Checking Office mocks...")
    try:
        mocks_dir = Path("mocks")
        required_mocks = ["word.html", "excel.html", "powerpoint.html"]
        
        found_mocks = []
        for mock_file in required_mocks:
            mock_path = mocks_dir / mock_file
            if mock_path.exists():
                found_mocks.append(mock_file)
        
        if len(found_mocks) == len(required_mocks):
            status['office_mocks'] = True
            print(f"   ✅ All {len(required_mocks)} Office mocks present")
        else:
            print(f"   ⚠️  {len(found_mocks)}/{len(required_mocks)} mocks found")
            
    except Exception as e:
        print(f"   ❌ Office mocks check failed: {e}")
    
    # 3. Check Server Status
    print("\\n3️⃣ Checking server status...")
    try:
        response = requests.get("http://localhost:8000", timeout=3)
        if response.status_code == 200:
            status['server_running'] = True
            print("   ✅ Flask server responding")
        else:
            print(f"   ⚠️  Server responded with {response.status_code}")
    except requests.exceptions.RequestException:
        print("   ⚠️  Server not accessible (may need restart)")
    except Exception as e:
        print(f"   ❌ Server check failed: {e}")
    
    # 4. Check Schema Validity
    print("\\n4️⃣ Checking schema validity...")
    try:
        schema_path = Path("schemas/office_tests.yaml")
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_data = yaml.safe_load(f)
            
            # Check structure
            if all(key in schema_data for key in ['metadata', 'tests']):
                if schema_data['tests'] and len(schema_data['tests']) > 0:
                    status['schemas_valid'] = True
                    print(f"   ✅ Schema valid with {len(schema_data['tests'])} tests")
                else:
                    print("   ⚠️  Schema has no test scenarios")
            else:
                print("   ⚠️  Schema missing required keys")
        else:
            print("   ❌ Schema file not found")
    except Exception as e:
        print(f"   ❌ Schema validation failed: {e}")
    
    # Summary
    print("\\n📊 PHASE 2 STATUS SUMMARY:")
    print("=" * 40)
    
    working_components = sum(status.values())
    total_components = len(status)
    
    for component, working in status.items():
        icon = "✅" if working else "❌"
        print(f"{icon} {component.replace('_', ' ').title()}")
    
    print(f"\\n🎯 Phase 2 Status: {working_components}/{total_components} components operational")
    
    if working_components == total_components:
        print("🌟 Phase 2 FULLY OPERATIONAL!")
        print("🚀 Ready for advanced testing and integration!")
    elif working_components >= 3:
        print("🟡 Phase 2 MOSTLY OPERATIONAL")
        print("🔧 Minor issues to resolve")
    else:
        print("🔴 Phase 2 NEEDS ATTENTION")
        print("🛠️  Several components need fixing")
    
    return status

def show_next_steps():
    """Show what we can do next."""
    print("\\n🚀 NEXT STEPS:")
    print("=" * 30)
    print("1. 🌐 Open Office mocks in browser:")
    print("   - Word: http://localhost:8000/mocks/word.html")
    print("   - Excel: http://localhost:8000/mocks/excel.html")
    print("   - PowerPoint: http://localhost:8000/mocks/powerpoint.html")
    print("\\n2. 🧪 Run YAML-driven tests:")
    print("   - python yaml_runner.py")
    print("\\n3. 📊 Generate reports:")
    print("   - python report_extender.py")
    print("\\n4. 🔄 Integration testing:")
    print("   - Test with InteractiveUXAgent")
    print("   - Visual regression testing")
    print("   - Performance benchmarking")

if __name__ == "__main__":
    status = check_phase2_status()
    show_next_steps()
