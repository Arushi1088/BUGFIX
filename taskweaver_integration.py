#!/usr/bin/env python3
"""
🔧 TaskWeaver Integration for UX Analyzer
Demonstrates how to use TaskWeaver for complex UX analysis workflows.
"""

import os
import json
from typing import Dict, List, Any
from task_weaver import (
    Task, TaskDefinition, TaskStatus, TaskPriority,
    BaseTaskExecutor, Server, configure_logging
)

class UXAnalysisTaskExecutor(BaseTaskExecutor):
    """Custom task executor for UX analysis workflows."""
    
    def __init__(self):
        super().__init__()
        self.name = "ux_analysis_executor"
    
    async def execute(self, task: Task) -> Dict[str, Any]:
        """Execute a UX analysis task."""
        task_type = task.definition.metadata.get("type", "unknown")
        
        if task_type == "url_analysis":
            return await self._execute_url_analysis(task)
        elif task_type == "batch_analysis":
            return await self._execute_batch_analysis(task)
        elif task_type == "comparison_analysis":
            return await self._execute_comparison_analysis(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def _execute_url_analysis(self, task: Task) -> Dict[str, Any]:
        """Execute single URL analysis."""
        url = task.definition.metadata.get("url")
        if not url:
            return {"error": "No URL provided"}
        
        # Import your existing analysis function
        from app_simple import analyze_url_simple
        
        result = analyze_url_simple(url)
        return {
            "status": "completed",
            "url": url,
            "analysis": result,
            "task_id": task.info.task_id
        }
    
    async def _execute_batch_analysis(self, task: Task) -> Dict[str, Any]:
        """Execute batch analysis of multiple URLs."""
        urls = task.definition.metadata.get("urls", [])
        if not urls:
            return {"error": "No URLs provided"}
        
        results = []
        for url in urls:
            # Create subtask for each URL
            subtask_def = TaskDefinition(
                name=f"analyze_{url.split('//')[1].split('/')[0]}",
                description=f"Analyze UX for {url}",
                metadata={"type": "url_analysis", "url": url}
            )
            
            # This would normally be submitted to the task manager
            # For demo, we'll call directly
            from app_simple import analyze_url_simple
            result = analyze_url_simple(url)
            results.append({"url": url, "result": result})
        
        return {
            "status": "completed",
            "batch_results": results,
            "total_analyzed": len(results),
            "task_id": task.info.task_id
        }
    
    async def _execute_comparison_analysis(self, task: Task) -> Dict[str, Any]:
        """Execute comparative analysis between multiple URLs."""
        urls = task.definition.metadata.get("urls", [])
        if len(urls) < 2:
            return {"error": "Need at least 2 URLs for comparison"}
        
        # Analyze each URL
        analyses = []
        for url in urls:
            from app_simple import analyze_url_simple
            result = analyze_url_simple(url)
            analyses.append({"url": url, "analysis": result})
        
        # Generate comparison report
        comparison = self._generate_comparison_report(analyses)
        
        return {
            "status": "completed",
            "comparison_report": comparison,
            "analyzed_urls": urls,
            "task_id": task.info.task_id
        }
    
    def _generate_comparison_report(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Generate a comparison report from multiple analyses."""
        # This is a simplified comparison - you could use AI to generate insights
        total_issues = sum(len(analysis["analysis"].get("data", [])) for analysis in analyses)
        
        return {
            "summary": f"Analyzed {len(analyses)} websites with {total_issues} total issues found",
            "individual_analyses": analyses,
            "recommendations": "Consider addressing common issues across all analyzed sites"
        }

def create_ux_analysis_tasks() -> List[TaskDefinition]:
    """Create example UX analysis task definitions."""
    tasks = []
    
    # Single URL analysis task
    single_task = TaskDefinition(
        name="analyze_single_url",
        description="Analyze UX for a single website URL",
        priority=TaskPriority.MEDIUM,
        metadata={
            "type": "url_analysis",
            "url": "https://example.com"
        }
    )
    tasks.append(single_task)
    
    # Batch analysis task
    batch_task = TaskDefinition(
        name="analyze_multiple_urls",
        description="Batch analyze multiple website URLs",
        priority=TaskPriority.HIGH,
        metadata={
            "type": "batch_analysis",
            "urls": [
                "https://example.com",
                "https://github.com",
                "https://stackoverflow.com"
            ]
        }
    )
    tasks.append(batch_task)
    
    # Comparison analysis task
    comparison_task = TaskDefinition(
        name="compare_websites",
        description="Compare UX between competitor websites",
        priority=TaskPriority.HIGH,
        metadata={
            "type": "comparison_analysis",
            "urls": [
                "https://amazon.com",
                "https://ebay.com"
            ]
        }
    )
    tasks.append(comparison_task)
    
    return tasks

def setup_taskweaver_for_ux_analysis():
    """Set up TaskWeaver configuration for UX analysis workflows."""
    
    # Configure logging
    configure_logging(level="INFO")
    
    # Load configuration
    config_path = "taskweaver_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✅ Loaded TaskWeaver config from {config_path}")
    else:
        print(f"⚠️ Config file {config_path} not found, using defaults")
        config = {}
    
    # Create task executor
    executor = UXAnalysisTaskExecutor()
    
    # Create example tasks
    tasks = create_ux_analysis_tasks()
    
    print(f"🚀 TaskWeaver UX Analysis setup complete!")
    print(f"📝 Created {len(tasks)} example task definitions")
    print(f"🔧 Custom executor: {executor.name}")
    
    return executor, tasks, config

if __name__ == "__main__":
    print("🔧 Setting up TaskWeaver for UX Analysis...")
    executor, tasks, config = setup_taskweaver_for_ux_analysis()
    
    print("\n📋 Available Task Definitions:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.name}: {task.description}")
        print(f"   Priority: {task.priority}")
        print(f"   Type: {task.metadata.get('type', 'unknown')}")
        print()
    
    print("🎯 TaskWeaver is ready for UX analysis workflows!")
    print("💡 You can now integrate these tasks into your Flask application.")
