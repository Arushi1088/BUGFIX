#!/bin/bash

# Phase 3 UX Analytics CI Test Script
echo "🚀 Running Phase 3 UX Analytics CI Tests"
echo "========================================"

# Function to cleanup on exit
cleanup() {
    echo "🧹 Cleaning up..."
    pkill -f "python.*server.py" 2>/dev/null || true
    kill $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT

# Change to ux-analyzer directory
cd "$(dirname "$0")"

# Check if required files exist
echo "📋 Checking required files..."
required_files=("server.py" "yaml_runner.py" "schemas/office_tests.yaml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file not found: $file"
        exit 1
    fi
    echo "   ✅ $file"
done

# Start mock server
echo "🌐 Starting mock server..."
python server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo "✅ Server is running"
else
    echo "❌ Server failed to start"
    exit 1
fi

# Run Phase 3 smoke test
echo "🧪 Running Phase 3 smoke test..."
python yaml_runner.py --config schemas/office_tests.yaml --filter "Integration Nav (Phase 3)"

if [ $? -eq 0 ]; then
    echo "✅ Smoke test passed"
    SMOKE_TEST_RESULT="PASS"
else
    echo "❌ Smoke test failed"
    SMOKE_TEST_RESULT="FAIL"
fi

# Run unit tests
echo "🧪 Running unit tests..."
python test_phase3_components.py

if [ $? -eq 0 ]; then
    echo "✅ Unit tests passed"
    UNIT_TEST_RESULT="PASS"
else
    echo "❌ Unit tests failed"
    UNIT_TEST_RESULT="FAIL"
fi

# Check for output files
echo "📁 Checking output files..."
if [ -d "reports" ] && [ "$(ls -A reports)" ]; then
    echo "✅ Report files generated"
    ls -la reports/
    FILES_RESULT="PASS"
else
    echo "❌ No report files found"
    FILES_RESULT="FAIL"
fi

# Final results
echo ""
echo "🎯 CI TEST RESULTS:"
echo "=================="
echo "   🧪 Smoke Test: $SMOKE_TEST_RESULT"
echo "   🔬 Unit Tests: $UNIT_TEST_RESULT"
echo "   📁 Files Generated: $FILES_RESULT"

# Determine overall result
if [ "$SMOKE_TEST_RESULT" = "PASS" ] && [ "$UNIT_TEST_RESULT" = "PASS" ] && [ "$FILES_RESULT" = "PASS" ]; then
    echo "   🏆 Overall: ✅ ALL TESTS PASSED!"
    exit 0
else
    echo "   🏆 Overall: ❌ SOME TESTS FAILED"
    exit 1
fi
