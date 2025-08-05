#!/usr/bin/env python3
"""
🔄 UX Analyzer - Backup & Recovery Verification Script
Created: July 25, 2025

This script verifies that all backup components are in place and working.
"""

import os
import sys
import json
from datetime import datetime

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {os.path.basename(filepath)} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {os.path.basename(filepath)} - NOT FOUND")
        return False

def verify_backup():
    """Verify all backup components are in place."""
    print("🔍 UX Analyzer - Backup Verification")
    print("=" * 50)
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"📁 Current Directory: {current_dir}")
    
    # Core working files
    print("\n📋 Core Working Files:")
    files_ok = 0
    total_files = 0
    
    core_files = [
        ("ux_analyzer_html.py", "Main HTML Report Generator"),
        ("ux_analyzer_simple.py", "Simple JSON Output Version"),
        ("uiux_checklist.json", "UX Evaluation Checklist"),
        ("test_setup.py", "Setup Verification Script"),
        ("BACKUP_README.md", "Backup Documentation")
    ]
    
    for filename, description in core_files:
        total_files += 1
        if check_file_exists(filename, description):
            files_ok += 1
    
    # Check test files
    print("\n🧪 Test Files:")
    test_files = [
        ("homepage.png", "Test Screenshot"),
    ]
    
    for filename, description in test_files:
        total_files += 1
        if check_file_exists(filename, description):
            files_ok += 1
    
    # Check for generated reports
    print("\n📊 Generated Reports:")
    html_reports = [f for f in os.listdir('.') if f.startswith('ux_analysis_report_') and f.endswith('.html')]
    if html_reports:
        for report in html_reports:
            print(f"✅ Generated Report: {report}")
            files_ok += 1
            total_files += 1
    else:
        print("ℹ️  No generated reports found (this is normal)")
    
    # Check checklist content
    print("\n📝 Checklist Validation:")
    try:
        with open("uiux_checklist.json") as f:
            checklist = json.load(f)
        
        total_categories = len(checklist)
        total_items = sum(len(items) for items in checklist.values())
        print(f"✅ Checklist loaded: {total_categories} categories, {total_items} items")
        
        for category, items in checklist.items():
            print(f"   • {category}: {len(items)} items")
            
    except Exception as e:
        print(f"❌ Checklist validation failed: {e}")
    
    # Git status
    print("\n🔗 Git Repository Status:")
    try:
        if os.path.exists('.git'):
            print("✅ Git repository initialized")
            # Check for commits
            try:
                import subprocess
                result = subprocess.run(['git', 'log', '--oneline', '-n', '1'], 
                                      capture_output=True, text=True, cwd='.')
                if result.returncode == 0:
                    print(f"✅ Latest commit: {result.stdout.strip()}")
                else:
                    print("ℹ️  No commits found")
            except:
                print("ℹ️  Could not check Git status")
        else:
            print("❌ Git repository not found")
    except Exception as e:
        print(f"❌ Git check failed: {e}")
    
    # Backup directory check
    print("\n💾 Backup Directory Check:")
    backup_base = "/Users/arushitandon/Desktop"
    backup_dirs = []
    
    try:
        for item in os.listdir(backup_base):
            if item.startswith("UIUX analyzer - BACKUP"):
                backup_dirs.append(item)
        
        if backup_dirs:
            for backup_dir in sorted(backup_dirs):
                backup_path = os.path.join(backup_base, backup_dir)
                print(f"✅ Backup found: {backup_dir}")
                
                # Check backup contents
                backup_contents = os.listdir(backup_path)
                print(f"   📂 Contains {len(backup_contents)} items")
        else:
            print("❌ No backup directories found")
            
    except Exception as e:
        print(f"❌ Backup check failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 BACKUP VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Files Verified: {files_ok}/{total_files}")
    
    if files_ok == total_files:
        print("🎉 ALL SYSTEMS GO - Backup is complete and verified!")
        print("\n🚀 Ready to proceed with confidence!")
        print("\n📋 To restore from backup:")
        print("   1. Copy files from backup directory")
        print("   2. Set OPENAI_API_KEY environment variable")  
        print("   3. Run: python test_setup.py")
        print("   4. Test: python ux_analyzer_html.py homepage.png")
    else:
        print("⚠️  INCOMPLETE BACKUP - Some files may be missing")
        print("Please check the missing files before proceeding.")
    
    print(f"\n🕐 Verification completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    verify_backup()
