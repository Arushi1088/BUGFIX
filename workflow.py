#!/usr/bin/env python3
"""
🔧 Simple Task Workflow for UX Analysis
Using a decorator-based pattern    # 1) If it's a "search for X" scenario, do the search generically:
    m = re.match(r'search for "(.+?)"(?: and (.+))?', scenario, flags=re.IGNORECASE)
    if m:
        query = m.group(1)
        print(f"🔍 Detected search query: {query}")
        
        # Dismiss overlays before searching (they might have appeared)
        await dismiss_overlays(page)
        
        # 2) find the search inputed by TaskWeaver but implemented simply.
Now using Playwright's Async API.
"""

import os
import base64
import functools
import re
import asyncio
from typing import Any, Callable, Dict, List
from dotenv import load_dotenv
from utils import run_ux_audit, plan_actions  # Import our audit entrypoint and action planner

# Load environment variables
load_dotenv()

# Search selectors for generic search functionality (prioritize site-specific over Google)
SEARCH_SELECTORS = [
    # E-commerce and site-specific search patterns (try these FIRST)
    'input[placeholder*="Search"]',
    'input[type="search"]',
    'input[name*="search"]',
    'input[id*="search"]',
    'input[class*="search"]',
    'input[aria-label*="Search"]',
    'input[title*="Search"]',
    'input[name="query"]',
    'input[name="keyword"]',
    'input[name="term"]',
    'input[placeholder*="Find"]',
    'input[placeholder*="Looking for"]',
    'input[placeholder*="What are you"]',
    # Shopify and e-commerce specific
    'input[name="q"]',
    'input.search-input',
    'input.search-field',
    'input#search',
    'input.search-box',
    # Generic text inputs (try last among visible inputs)
    'input[type="text"]',
    # Google-specific (ONLY if we're actually on Google)
    'input.gLFyf',                   
    'input.gsfi',                    
    'input[aria-label*="Search Google"]'
]

# Simple task registry
TASK_REGISTRY: Dict[str, Callable] = {}

async def dismiss_overlays(page):
    """Dismiss common overlays like cookie banners and sign-in dialogs."""
    print("🚫 Dismissing overlays...")
    
    # Wait a moment for overlays to appear
    await page.wait_for_timeout(1000)
    
    # Cookie banner and consent dialogs
    for btn_text in ("I agree", "Accept all", "OK", "Accept", "Got it", "Allow all", "Agree"):
        btn = page.locator(f"button:has-text('{btn_text}')")
        count = await btn.count()
        if count > 0:
            try:
                print(f"  ↳ Found and clicking '{btn_text}' button...")
                await btn.first.click(timeout=5000)
                await page.wait_for_timeout(500)
            except Exception as e:
                print(f"  ↳ Failed to click '{btn_text}' button: {e}")
        else:
            print(f"  ↳ No '{btn_text}' button found")
    
    # Generic modal-close (X) buttons and rejection options
    close_selectors = [
        "button[aria-label='Close']",
        "button:has-text('No thanks')",
        "button:has-text('Not now')", 
        "button:has-text('Skip')",
        "button:has-text('Maybe later')",
        "[data-testid='close-button']",
        ".close-button",
        "[aria-label='Dismiss']"
    ]
    
    for selector in close_selectors:
        close = page.locator(selector)
        count = await close.count()
        if count > 0:
            try:
                print(f"  ↳ Found and clicking close button: {selector}")
                # Use shorter timeout and force click if needed
                await close.first.click(timeout=5000, force=True)
                await page.wait_for_timeout(500)
            except Exception as e:
                print(f"  ↳ Failed to click close button {selector}: {e}")
        else:
            print(f"  ↳ No close button found: {selector}")
    
    print("✅ Overlay dismissal completed")

def step(func: Callable) -> Callable:
    """Simple step decorator to register async workflow tasks."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"🔧 Executing step: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            print(f"✅ Step completed: {func.__name__}")
            return result
        except Exception as e:
            print(f"❌ Step failed: {func.__name__} - {e}")
            raise
    
    # Register the task
    TASK_REGISTRY[func.__name__] = wrapper
    return wrapper

@step
async def open_page(url: str):
    """⚠️ Create a fresh Playwright per invocation using async API with enhanced resilience"""
    from playwright.async_api import async_playwright
    
    print(f"🌐 Opening page: {url}")
    play = await async_playwright().start()
    browser = await play.chromium.launch(headless=False)
    
    # 1) Create context with a "real" user-agent so fewer sites block headless
    ctx = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        locale="en-US",
    )
    page = await ctx.new_page()
    
    # 2) Block heavy/tracking resources to speed up load & avoid endless ads (but allow some for screenshots)
    async def route_handler(route, request):
        if request.resource_type in {"font", "media"}:  # Only block heavy media, keep images/CSS for screenshots
            return await route.abort()
        return await route.continue_()
    await page.route("**/*", route_handler)
    
    # 3) Try networkidle → fallback to domcontentloaded
    try:
        await page.goto(url, wait_until="networkidle", timeout=60_000)
    except Exception:
        print("  ↳ networkidle timed out, retrying domcontentloaded…")
        await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    
    # 4) Short pause & dismiss overlays
    await page.wait_for_timeout(1_000)
    await dismiss_overlays(page)
    print("✅ Page loaded:", page.url)
    
    # Return all resources so later steps can close them
    return {"play": play, "browser": browser, "ctx": ctx, "page": page}

@step
async def perform_task(context: dict, scenario: str):
    """Perform a task on the page based on scenario using smart search detection or AI planning."""
    page = context["page"]
    print(f"🎯 Performing task: {scenario}")

    # 1) Dismiss overlays first (but don't let failures kill the workflow)
    try:
        await dismiss_overlays(page)
    except Exception as e:
        print(f"⚠️ Overlay dismissal failed, but continuing: {e}")
    
    # Wait a bit more for page to fully load
    await page.wait_for_timeout(2000)

    # 2) Enhanced search detection - catch more search patterns
    search_patterns = [
        r'search\s+for\s+["\']?([^"\']+?)["\']?(?:\s|$)',   # "search for dress"
        r'find\s+["\']?([^"\']+?)["\']?(?:\s|$)',          # "find dress" 
        r'look\s+for\s+["\']?([^"\']+?)["\']?(?:\s|$)',    # "look for dress"
        r'search\s+["\']?([^"\']+?)["\']?(?:\s|$)',        # "search dress"
        r'shop\s+for\s+["\']?([^"\']+?)["\']?(?:\s|$)',    # "shop for dress"
        r'browse\s+for\s+["\']?([^"\']+?)["\']?(?:\s|$)',  # "browse for dress"
    ]
    
    query = None
    for pattern in search_patterns:
        m = re.search(pattern, scenario, flags=re.IGNORECASE)
        if m:
            query = m.group(1).strip()
            print(f"🔍 Detected search query: {query!r} using pattern: {pattern}")
            break
    
    if query:
        # 3) Smart search - try site-specific search FIRST, avoid Google unless necessary
        search_filled = False
        current_url = page.url.lower()
        
        # Filter selectors based on current site
        if 'google.com' in current_url:
            # If we're already on Google, use Google selectors
            relevant_selectors = [s for s in SEARCH_SELECTORS if 'google' in s.lower() or 'gLFyf' in s or 'gsfi' in s]
            print("🔍 On Google - using Google-specific selectors")
        else:
            # If we're on the target site, avoid Google selectors and prioritize site-specific ones
            relevant_selectors = [s for s in SEARCH_SELECTORS if 'google' not in s.lower() and 'gLFyf' not in s and 'gsfi' not in s]
            print(f"🔍 On target site ({current_url}) - using site-specific selectors")
        
        # Try the filtered selectors first
        for sel in relevant_selectors:
            try:
                print(f"  ↳ trying selector: {sel}")
                await page.wait_for_selector(sel, state="visible", timeout=10_000)  # Reduced timeout
                await page.fill(sel, query)
                print(f"  ✅ filled search box with: {query}")
                search_filled = True
                break
            except Exception as e:
                print(f"    ✖ selector failed: {sel} - {str(e)}")
                continue
        
        # 4) Enhanced JS fallback - look for any visible search-like input
        if not search_filled:
            print("🔍 Standard selectors failed - trying enhanced JS fallback")
            try:
                # Look for inputs with search-related attributes
                search_inputs = await page.evaluate("""
                    () => {
                        const inputs = Array.from(document.querySelectorAll('input'));
                        return inputs
                            .filter(input => {
                                const style = window.getComputedStyle(input);
                                const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && input.offsetParent !== null;
                                const hasSearchAttrs = 
                                    input.placeholder?.toLowerCase().includes('search') ||
                                    input.name?.toLowerCase().includes('search') ||
                                    input.id?.toLowerCase().includes('search') ||
                                    input.className?.toLowerCase().includes('search') ||
                                    input.type === 'search' ||
                                    input.getAttribute('aria-label')?.toLowerCase().includes('search');
                                return isVisible && hasSearchAttrs;
                            })
                            .map(input => ({
                                selector: input.tagName.toLowerCase() + 
                                         (input.id ? '#' + input.id : '') +
                                         (input.className ? '.' + input.className.split(' ').join('.') : ''),
                                placeholder: input.placeholder,
                                name: input.name
                            }));
                    }
                """)
                
                if search_inputs:
                    print(f"  ✅ Found {len(search_inputs)} search-like inputs via JS")
                    for input_info in search_inputs[:3]:  # Try first 3
                        try:
                            selector = input_info['selector']
                            await page.fill(selector, query)
                            search_filled = True
                            print(f"  ✅ JS search filled: {selector}")
                            break
                        except Exception as e:
                            print(f"  ✖ JS search failed for {selector}: {e}")
                            continue
                
                # If still no luck, try any visible text input as last resort
                if not search_filled:
                    handle = await page.query_selector("input[type='text']:visible, input:not([type]):visible")
                    if handle:
                        await page.evaluate(
                            """(el, v) => { el.focus(); el.value = v; el.dispatchEvent(new Event('input', {bubbles: true})); }""",
                            handle, query
                        )
                        search_filled = True
                        print("  ✅ Generic input fallback succeeded")
                    else:
                        print("  ✖ No visible inputs found via JS")
                        
            except Exception as e:
                print(f"  ✖ Enhanced JS fallback failed: {e}")
        
        # 5) LAST RESORT: Google search (only if we couldn't find search on the target site)
        if not search_filled and 'google.com' not in current_url:
            from urllib.parse import quote
            print("  ⚠️ Last resort: redirecting to Google search")
            print(f"  📍 Original site didn't have detectable search: {current_url}")
            await page.goto(f"https://www.google.com/search?q={quote(query)}", wait_until="networkidle")
            await dismiss_overlays(page)
            search_filled = True  # We're now on Google search results
        
        # 6) Submit & navigate (if we filled a search box on the original site)
        if search_filled and 'google.com' not in current_url:
            try:
                await page.keyboard.press("Enter")
                print("⏳ Waiting for search results on original site...")
                await page.wait_for_load_state("networkidle", timeout=30000)
                
                # Try to click on a product/result if this looks like an e-commerce site
                await page.wait_for_timeout(2000)  # Let results load
                
                # Look for product links or search results to click
                product_selectors = [
                    'a[href*="/product"]',
                    'a[href*="/item"]', 
                    'a[href*="/p/"]',
                    '.product-item a',
                    '.search-result a',
                    '.product a',
                    'article a',
                    '.result a'
                ]
                
                clicked_result = False
                for sel in product_selectors:
                    try:
                        result_link = page.locator(sel).first
                        if await result_link.count() > 0:
                            await result_link.scroll_into_view_if_needed()
                            await result_link.click()
                            print(f"🔗 Clicked search result: {sel}")
                            await page.wait_for_load_state("networkidle", timeout=30000)
                            clicked_result = True
                            break
                    except Exception as e:
                        print(f"  ✖ Could not click {sel}: {e}")
                        continue
                
                if not clicked_result:
                    print("📝 No clickable results found, staying on search results page")
                    
            except Exception as e:
                print(f"⚠️ Search submit failed, but continuing: {e}")
        elif 'google.com' in page.url.lower():
            # We're on Google, try to click first result
            print("🔗 On Google - trying to click first result")
            try:
                first_result = page.locator("h3").first
                if await first_result.count() > 0:
                    await first_result.click()
                    print("⏳ Waiting for result page to load...")
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    print("✅ Clicked Google result successfully")
                else:
                    print("📝 No Google results found to click")
            except Exception as e:
                print(f"⚠️ Could not click Google result: {e}")
                print("📝 Continuing with Google search results page for analysis")
        
        return context

    # — otherwise, fall back to LLM-driven planner —
    print("🤖 Using AI planner for scenario")
    try:
        steps = plan_actions(scenario)  # existing sync LLM call
        print("🛠️ DEBUG - Planned Steps:", steps)   # DEBUG: Show full planner output
        print(f"📋 Planned {len(steps)} actions")
        
        for idx, s in enumerate(steps, start=1):
            act, sel, val = s["action"], s["selector"], s["value"]
            print(f"🔧 Step {idx}: {act} – {sel or 'N/A'} – {val or 'N/A'}")
            
            if act == "goto":
                try:
                    await page.goto(val, wait_until="networkidle", timeout=60_000)
                except Exception:
                    print(f"  ↳ networkidle timed out for {val}, retrying domcontentloaded…")
                    await page.goto(val, wait_until="domcontentloaded", timeout=60_000)
                # Dismiss overlays after navigation
                await dismiss_overlays(page)
            elif act == "click":
                await page.wait_for_selector(sel, timeout=10_000)
                await page.click(sel)
            elif act == "fill":
                await page.wait_for_selector(sel, state="visible", timeout=10_000)
                await page.fill(sel, val)  # Use fill instead of click + type
            elif act == "press":
                if sel:
                    try:
                        await page.wait_for_selector(sel, timeout=5_000)
                        await page.click(sel)
                    except:
                        pass
                await page.keyboard.press(val or "Enter")
            elif act == "wait":
                await page.wait_for_selector(sel, timeout=10_000)
            await page.wait_for_timeout(500)
        
        print(f"✅ All {len(steps)} actions completed successfully")
    
    except Exception as e:
        print(f"⚠️ AI planner failed: {e}")
        print("📝 Continuing with current page for analysis")
    
    return context

@step
async def snapshot_and_audit(context: dict):
    """Take a screenshot and perform UX audit."""
    page = context["page"]
    print("📸 Taking screenshot...")
    
    try:
        # Wait a moment for page to stabilize after navigation
        await page.wait_for_timeout(2000)
        
        # Check if page is still accessible
        if page.is_closed():
            print("⚠️ Page is closed, cannot take screenshot")
            return {"status": "error", "error": "Page was closed before screenshot"}
        
        png_bytes = await page.screenshot(full_page=True, timeout=30000)
        print(f"📸 Screenshot captured, size: {len(png_bytes)} bytes")
        
        # Call our audit function from utils.py
        audit_result = run_ux_audit(png_bytes)
        print("📊 UX audit completed")
        return audit_result
        
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        print("📝 Continuing with page content analysis instead")
        
        # Fallback: analyze page content without screenshot
        try:
            content = await page.content()
            audit_result = run_ux_audit(content.encode('utf-8'))
            print("📊 Content-based UX audit completed")
            return audit_result
        except Exception as e2:
            print(f"❌ Content analysis also failed: {e2}")
            return {"status": "error", "error": f"Both screenshot and content analysis failed: {e}, {e2}"}

@step
async def close(context: dict):
    """⚡️ tear down *this* Playwright instance cleanly"""
    print("🔒 Closing resources...")
    await context["page"].close()
    if "ctx" in context:
        await context["ctx"].close()
    await context["browser"].close()
    await context["play"].stop()
    print("✅ All resources closed")
    return "closed"

# TaskWeaver workflow functions
async def analyze_website_workflow(url: str, scenario: str = None):
    """
    Runs the workflow on the given URL + scenario description.
    Returns the analysis result.
    """
    print(f"🚀 Starting UX analysis workflow for: {url}")
    if scenario:
        print(f"📝 Scenario: {scenario}")
    
    try:
        # Step 1: Open the page and get context
        context = await open_page(url)
        
        # Step 2: Perform the scenario task (if provided) or default task
        if scenario:
            context = await perform_task(context, scenario)
        else:
            context = await perform_task(context, "Wait for page to fully load and stabilize")
        
        # Step 3: Take screenshot and audit
        audit_result = await snapshot_and_audit(context)
        
        # Step 4: Close all resources
        close_result = await close(context)
        
        print("✅ Workflow completed successfully!")
        return audit_result
        
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return {"status": "error", "error": str(e)}

async def batch_analyze_workflow(urls: list):
    """Analyze multiple websites in sequence."""
    print(f"🚀 Starting batch analysis for {len(urls)} websites...")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n📊 Analyzing website {i}/{len(urls)}: {url}")
        result = await analyze_website_workflow(url)  # No scenario for batch analysis
        results.append({"url": url, "result": result})
    
    print(f"✅ Batch analysis completed! Analyzed {len(results)} websites.")
    return results

def cleanup_browser():
    """Clean up browser resources (no longer needed with per-invocation instances)."""
    print("🧹 Browser cleanup no longer needed - resources cleaned per workflow")
    print("✅ Each workflow cleans up its own Playwright instance")

def run_workflow(url: str, scenario: str = None) -> dict:
    """
    Synchronous wrapper for the enhanced workflow that can be called from Flask.
    """
    async def _run():
        return await analyze_website_workflow(url, scenario)
    
    return asyncio.run(_run())

if __name__ == "__main__":
    print("🔧 TaskWeaver UX Analysis Workflow Ready!")
    print("📋 Available functions:")
    print("  - analyze_website_workflow(url, scenario=None)")
    print("  - batch_analyze_workflow([url1, url2, ...])")
    print("  - cleanup_browser()")
    
    # Example usage
    async def main():
        test_url = "https://example.com"
        test_scenario = "Click on the 'More information...' link"
        print(f"\n🧪 Testing with: {test_url}")
        print(f"📝 Scenario: {test_scenario}")
        
        try:
            result = await analyze_website_workflow(test_url, test_scenario)
            print("\n📊 Analysis Result:")
            print(f"Status: {result.get('status', 'unknown')}")
            if result.get('status') == 'success':
                print(f"Data length: {len(result.get('data', ''))} characters")
                print(f"Screenshot size: {len(result.get('screenshot', ''))} bytes")
            else:
                print(f"Error: {result.get('error', 'unknown error')}")
        
        except Exception as e:
            print(f"❌ Test failed: {e}")
        finally:
            cleanup_browser()
    
    # Run the async main function
    asyncio.run(main())
