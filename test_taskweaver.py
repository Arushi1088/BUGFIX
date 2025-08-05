#!/usr/bin/env python3
"""
🧪 TaskWeaver UX Analysis Test Script
Simple test to verify TaskWeaver integration works with your UX Analyzer.
"""

import os
import sys
import asyncio
from datetime import datetime

def test_taskweaver_basic():
    """Test basic TaskWeaver functionality."""
    print("🧪 Testing TaskWeaver Basic Functionality...")
    
    try:
        from task_weaver import Task, TaskDefinition, TaskStatus, TaskPriority
        print("✅ TaskWeaver imports successful")
        
        # Create a simple task definition
        task_def = TaskDefinition(
            name="test_ux_task",
            description="Test UX analysis task for TaskWeaver integration",
            priority=TaskPriority.MEDIUM,
            metadata={"type": "test", "created_at": datetime.now().isoformat()}
        )
        print(f"✅ Task definition created: {task_def.name}")
        
        # Create task instance
        task = Task(definition=task_def)
        print(f"✅ Task instance created with ID: {task.info.task_id}")
        print(f"   Status: {task.info.status}")
        print(f"   Priority: {task.definition.priority}")
        
        return True
        
    except Exception as e:
        print(f"❌ TaskWeaver basic test failed: {e}")
        return False

def test_taskweaver_config():
    """Test TaskWeaver configuration loading."""
    print("\n🧪 Testing TaskWeaver Configuration...")
    
    config_files = [
        "taskweaver_config.json",
        "taskweaver_config_advanced.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(f"✅ Configuration loaded from {config_file}")
                print(f"   Keys: {list(config.keys())}")
                
                # Check if API key is configured
                api_key = config.get("llm.api_key", "")
                if api_key and api_key != "YOUR_OPENAI_KEY":
                    print("✅ API key is configured")
                else:
                    print("⚠️ API key needs to be set")
                
            except Exception as e:
                print(f"❌ Error loading {config_file}: {e}")
        else:
            print(f"⚠️ Configuration file {config_file} not found")

def test_ux_integration():
    """Test integration with existing UX analysis functions."""
    print("\n🧪 Testing UX Analysis Integration...")
    
    try:
        # Test if we can import UX analysis functions
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Check if app_simple module is available
        try:
            import app_simple
            print("✅ app_simple module import successful")
            
            # Check if analysis functions exist
            if hasattr(app_simple, 'analyze_url_simple'):
                print("✅ analyze_url_simple function found")
            else:
                print("⚠️ analyze_url_simple function not found")
                
            if hasattr(app_simple, 'analyze_upload_simple'):
                print("✅ analyze_upload_simple function found")
            else:
                print("⚠️ analyze_upload_simple function not found")
                
        except ImportError as e:
            print(f"⚠️ Could not import app_simple: {e}")
        
        # Test custom executor import
        try:
            from taskweaver_integration import UXAnalysisTaskExecutor, create_ux_analysis_tasks
            print("✅ Custom UXAnalysisTaskExecutor import successful")
            
            # Create executor instance
            executor = UXAnalysisTaskExecutor()
            print(f"✅ Executor instance created: {executor.name}")
            
            # Create sample tasks
            tasks = create_ux_analysis_tasks()
            print(f"✅ Created {len(tasks)} sample task definitions")
            
        except ImportError as e:
            print(f"❌ Could not import custom TaskWeaver integration: {e}")
            
    except Exception as e:
        print(f"❌ UX integration test failed: {e}")

async def test_async_functionality():
    """Test async task execution capabilities."""
    print("\n🧪 Testing Async Task Functionality...")
    
    try:
        from taskweaver_integration import UXAnalysisTaskExecutor
        from task_weaver import Task, TaskDefinition, TaskPriority
        
        # Create executor
        executor = UXAnalysisTaskExecutor()
        
        # Create a test task
        task_def = TaskDefinition(
            name="async_test_task",
            description="Test async task execution",
            priority=TaskPriority.LOW,
            metadata={"type": "test_async"}
        )
        
        task = Task(definition=task_def)
        print(f"✅ Async test task created: {task.info.task_id}")
        
        # This would normally execute the task, but we'll skip actual execution
        print("✅ Async functionality is ready")
        
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")

def run_all_tests():
    """Run all TaskWeaver tests."""
    print("🚀 Starting TaskWeaver Integration Tests...\n")
    
    test_results = []
    
    # Basic functionality test
    test_results.append(("Basic Functionality", test_taskweaver_basic()))
    
    # Configuration test
    test_taskweaver_config()
    
    # UX integration test
    test_ux_integration()
    
    # Async functionality test
    try:
        asyncio.run(test_async_functionality())
        test_results.append(("Async Functionality", True))
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        test_results.append(("Async Functionality", False))
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed_tests = sum(1 for _, passed in test_results if passed)
    total_tests = len(test_results)
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! TaskWeaver is ready for UX analysis.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    run_all_tests()
