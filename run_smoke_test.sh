#!/bin/bash
# 🚀 Comprehensive Smoke Test Runner
# Runs all Office mock verifications

echo "🎯 COMPREHENSIVE OFFICE MOCKS SMOKE TEST"
echo "=========================================="

# Navigate to project directory
cd "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer"
echo "📁 Working directory: $(pwd)"

# Check Python environment
PYTHON_CMD="/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer/.venv/bin/python"
echo "🐍 Python: $PYTHON_CMD"

# Step 1: Start server
echo ""
echo "1️⃣ Starting Office Mocks Server..."
$PYTHON_CMD server.py &
SERVER_PID=$!
echo "🌐 Server PID: $SERVER_PID"

# Wait for server to start
echo "⏳ Waiting for server startup..."
sleep 5

# Step 2: Test server connectivity
echo ""
echo "2️⃣ Testing server connectivity..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is responding"
else
    echo "❌ Server not responding"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Step 3: Run quick connectivity test
echo ""
echo "3️⃣ Running quick connectivity test..."
$PYTHON_CMD tests/quick_mock_test.py

# Step 4: Run Word mock test
echo ""
echo "4️⃣ Running Word mock verification..."
$PYTHON_CMD tests/verify_word_mock.py

# Step 5: Run Excel mock test
echo ""
echo "5️⃣ Running Excel mock verification..."
$PYTHON_CMD tests/verify_excel_mock.py

# Step 6: Run PowerPoint mock test
echo ""
echo "6️⃣ Running PowerPoint mock verification..."
$PYTHON_CMD tests/verify_powerpoint_mock.py

# Step 7: Run YAML system test
echo ""
echo "7️⃣ Testing YAML system..."
$PYTHON_CMD -c "
import yaml
print('✅ YAML module working')
with open('schemas/office_tests.yaml', 'r') as f:
    data = yaml.safe_load(f)
print(f'✅ YAML schema loaded: {len(data.get(\"tests\", []))} tests')
"

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null
echo "✅ Server stopped"

echo ""
echo "🎉 COMPREHENSIVE SMOKE TEST COMPLETE!"
echo "📊 Check output above for detailed results"
