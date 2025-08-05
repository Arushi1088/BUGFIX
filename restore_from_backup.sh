#!/bin/bash
# 🔄 UX Analyzer - Quick Restore Script
# Usage: ./restore_from_backup.sh

echo "🔄 UX Analyzer - Restore from Backup"
echo "===================================="

# Set variables
BACKUP_DIR="/Users/arushitandon/Desktop/UIUX analyzer - BACKUP - 20250725_093757"
RESTORE_DIR="/Users/arushitandon/Desktop/UIUX analyzer - RESTORED"

# Check if backup exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    echo "Available backups:"
    ls -la "/Users/arushitandon/Desktop" | grep "UIUX analyzer - BACKUP"
    exit 1
fi

echo "📁 Found backup: $BACKUP_DIR"

# Create restore directory
echo "📂 Creating restore directory..."
mkdir -p "$RESTORE_DIR"

# Copy backup contents
echo "📋 Copying files from backup..."
cp -r "$BACKUP_DIR"/* "$RESTORE_DIR"/

echo "✅ Restore completed!"
echo "📍 Restored to: $RESTORE_DIR"
echo ""
echo "🚀 Next steps:"
echo "1. cd '$RESTORE_DIR/ux-analyzer'"
echo "2. export OPENAI_API_KEY='your-api-key-here'"
echo "3. python test_setup.py"
echo "4. python ux_analyzer_html.py homepage.png"
echo ""
echo "🎉 Your UX Analyzer is ready to use!"
