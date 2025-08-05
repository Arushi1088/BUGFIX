#!/bin/bash
cd "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer"
echo "🚀 Starting dashboard server..."
echo "📁 Current directory: $(pwd)"
echo "📊 Available files:"
ls -la *.html
echo ""
echo "🌐 Starting server on http://localhost:8000"
python3 -m http.server 8000
