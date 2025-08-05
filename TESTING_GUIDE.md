# 🧪 Manual Testing Guide - SYSTEMATIC APPROACH

## Current Status
- ✅ Server running on localhost:8000 (manually started)
- ✅ Office mocks enhanced with data-testid attributes
- ✅ Playwright waits optimized (networkidle → load)
- ✅ YAML schema updated with proper selectors
- ✅ Context optimization implemented

## Step-by-Step Testing Procedure

### 1. Verify Server Status
```bash
# Test server connectivity
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","port":8000,"mocks_available":["word.html","excel.html","powerpoint.html"],"ready_for_testing":true}
```

### 2. Test Individual Mocks in Browser
```bash
# Open each mock manually to verify they load
open http://localhost:8000/mocks/word.html
open http://localhost:8000/mocks/excel.html
open http://localhost:8000/mocks/powerpoint.html
```

**Verify these elements are present:**
- Word: `[data-testid='new-doc-btn']`, `[data-testid='editor']`
- Excel: `[data-testid='cell-A1']`, `[data-testid='sum-btn']`
- PowerPoint: `[data-testid='slide-title']`, `[data-testid='new-slide-btn']`

### 3. Run Enhanced Agent Test
```bash
# In new terminal (keep server running in another)
cd "/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer"
python enhanced_mock_test.py
```

**Expected Output:**
```
🔍 ENHANCED MOCK TEST - OPTIMIZED FOR CONTEXT
📡 Testing server health...
✅ Server healthy: {'status': 'healthy', 'port': 8000}
📄 TESTING WORD MOCK (Context Optimized)
✅ Word test completed in X.XXs
📊 TESTING EXCEL MOCK (Cell Targeting)
✅ Excel test completed in X.XXs
🎉 ALL ENHANCED TESTS PASSED!
```

### 4. Run YAML-Driven Tests
```bash
python yaml_runner.py
```

**Expected:**
- YAML schema loaded successfully
- Word tests: 2 scenarios
- Excel tests: 2 scenarios
- PowerPoint tests: 2 scenarios

### 5. Troubleshooting Common Issues

#### Issue: "Connection refused" 
**Solution:** 
```bash
# Check if server is running
ps aux | grep python | grep 8000

# If not running, start it:
python robust_server.py
```

#### Issue: "Element not found"
**Solution:**
1. Open mock in browser
2. Open DevTools (F12)
3. Run: `document.querySelector('[data-testid="new-doc-btn"]')`
4. Verify element exists

#### Issue: "Timeout on goto"
**Solution:**
- Already fixed: wait_until="load" (not "networkidle")
- Verify mock loads in browser first

#### Issue: "Token limit exceeded"
**Solution:**
- Already optimized: reduced screenshot frequency
- Context summarization implemented
- Only last 3 actions shown

### 6. Verification Checklist

**Server Status:**
- [ ] Server responds to /health
- [ ] All 3 mocks load in browser
- [ ] No 404 errors

**Mock Elements:**
- [ ] Word mock has data-testid attributes
- [ ] Excel mock has cell targeting
- [ ] PowerPoint mock has slide elements

**Agent Tests:**
- [ ] Enhanced test runs without connection errors
- [ ] Word mock test completes
- [ ] Excel mock test completes
- [ ] No timeout errors

**YAML Tests:**
- [ ] YAML file loads successfully
- [ ] Performance metrics calculated
- [ ] All scenarios execute

### 7. Next Steps After Success

1. **Full Comprehensive Test:**
   ```bash
   python tests/verify_all_mocks.py
   ```

2. **Performance Validation:**
   ```bash
   python report_extender.py
   ```

3. **Phase 2 Completion:**
   - Document successful agent-driven Office automation
   - Commit Phase 2 enhancements
   - Prepare for production deployment

## Quick Reference Commands

```bash
# Start server (if needed)
python robust_server.py

# Quick connectivity test
curl http://localhost:8000/health

# Run optimized agent test
python enhanced_mock_test.py

# Run YAML-driven tests
python yaml_runner.py

# Check server process
ps aux | grep python | grep 8000

# Stop server process
pkill -f "python.*8000"
```

## Success Criteria

✅ **Connectivity:** All curl commands return 200
✅ **Agent Integration:** InteractiveUXAgent can drive Office mocks
✅ **Selector Targeting:** data-testid attributes work reliably  
✅ **Performance:** Tests complete in under 30 seconds each
✅ **Context Management:** No token limit errors
✅ **YAML Execution:** Schema-driven tests run successfully

When all criteria are met, Phase 2 is complete and ready for production!
