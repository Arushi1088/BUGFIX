
import time
import json
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class PerformanceMetric:
    """Structured performance metric data"""
    timestamp: float
    action: str
    lcp: Optional[float] = None
    fid: Optional[float] = None  
    cls: Optional[float] = None
    ttfb: Optional[float] = None
    dom_content_loaded: Optional[float] = None
    load_complete: Optional[float] = None
    fcp: Optional[float] = None
    memory_used: Optional[int] = None
    memory_total: Optional[int] = None
    action_latency: Optional[float] = None

class EnhancedInteractiveUXAgent:
    """Enhanced UX Agent with comprehensive performance monitoring"""

    def __init__(self, original_agent):
        self.agent = original_agent
        self.performance_log: List[PerformanceMetric] = []
        self.accessibility_results: List[Dict] = []
        self.keyboard_nav_data: List[Dict] = []
        self.screenshots_with_context: List[Dict] = []

    async def inject_performance_monitoring(self, page):
        """Inject Core Web Vitals and performance monitoring into the page"""

        # Core Web Vitals collection script
        monitoring_script = """
        window.performanceMetrics = {
            lcp: null,
            fid: null,
            cls: null,
            clsEntries: []
        };

        // Largest Contentful Paint (LCP)
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            window.performanceMetrics.lcp = lastEntry.startTime;
        }).observe({entryTypes: ['largest-contentful-paint']});

        // First Input Delay (FID)
        new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                if (entry.name === 'first-input') {
                    window.performanceMetrics.fid = entry.processingStart - entry.startTime;
                }
            }
        }).observe({entryTypes: ['first-input'], buffered: true});

        // Cumulative Layout Shift (CLS)
        new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                if (!entry.hadRecentInput) {
                    window.performanceMetrics.clsEntries.push(entry.value);
                    window.performanceMetrics.cls = window.performanceMetrics.clsEntries.reduce((sum, val) => sum + val, 0);
                }
            }
        }).observe({entryTypes: ['layout-shift']});

        // Helper function to get all metrics
        window.getAllPerformanceMetrics = () => {
            const navigation = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');

            return {
                // Core Web Vitals
                lcp: window.performanceMetrics.lcp,
                fid: window.performanceMetrics.fid,
                cls: window.performanceMetrics.cls,

                // Network Performance
                ttfb: navigation ? navigation.responseStart - navigation.requestStart : null,
                domContentLoaded: navigation ? navigation.domContentLoadedEventEnd : null,
                loadComplete: navigation ? navigation.loadEventEnd : null,

                // Paint Timing
                fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime || null,

                // Memory (if available)
                memory: performance.memory ? {
                    used: performance.memory.usedJSHeapSize,
                    total: performance.memory.totalJSHeapSize,
                    limit: performance.memory.jsHeapSizeLimit
                } : null,

                // Additional metrics
                navigationTiming: navigation ? {
                    redirectTime: navigation.redirectEnd - navigation.redirectStart,
                    dnsTime: navigation.domainLookupEnd - navigation.domainLookupStart,
                    connectTime: navigation.connectEnd - navigation.connectStart,
                    requestTime: navigation.responseEnd - navigation.requestStart,
                    responseTime: navigation.responseEnd - navigation.responseStart,
                    domParseTime: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                    loadTime: navigation.loadEventEnd - navigation.loadEventStart
                } : null
            };
        };
        """

        await page.evaluate(monitoring_script)
        print("✅ Performance monitoring injected into page")

    async def track_action_performance(self, action_name: str, action_func, page):
        """Track performance metrics for a specific action"""
        print(f"📊 Tracking performance for action: {action_name}")

        # Record start time
        start_time = time.time()

        # Execute the action
        await action_func()

        # Wait for network to settle
        await page.wait_for_load_state('networkidle', timeout=10000)

        # Record end time
        end_time = time.time()
        action_latency = (end_time - start_time) * 1000  # Convert to ms

        # Collect performance metrics
        try:
            metrics_data = await page.evaluate('window.getAllPerformanceMetrics()')

            # Create performance metric record
            metric = PerformanceMetric(
                timestamp=start_time,
                action=action_name,
                lcp=metrics_data.get('lcp'),
                fid=metrics_data.get('fid'),
                cls=metrics_data.get('cls'),
                ttfb=metrics_data.get('ttfb'),
                dom_content_loaded=metrics_data.get('domContentLoaded'),
                load_complete=metrics_data.get('loadComplete'),
                fcp=metrics_data.get('fcp'),
                memory_used=metrics_data.get('memory', {}).get('used') if metrics_data.get('memory') else None,
                memory_total=metrics_data.get('memory', {}).get('total') if metrics_data.get('memory') else None,
                action_latency=action_latency
            )

            self.performance_log.append(metric)

            print(f"✅ Performance tracked - Latency: {action_latency:.2f}ms")
            if metric.lcp:
                print(f"   LCP: {metric.lcp:.2f}ms")
            if metric.ttfb:
                print(f"   TTFB: {metric.ttfb:.2f}ms")
            if metric.cls:
                print(f"   CLS: {metric.cls:.4f}")

        except Exception as e:
            print(f"⚠️ Error collecting performance metrics: {e}")
            # Still record basic latency
            metric = PerformanceMetric(
                timestamp=start_time,
                action=action_name,
                action_latency=action_latency
            )
            self.performance_log.append(metric)

    async def capture_accessibility_scan(self, page, context_name: str):
        """Capture accessibility scan using axe-core"""
        print(f"♿ Running accessibility scan for: {context_name}")

        try:
            # Inject axe-core
            await page.evaluate("""
                if (!window.axe) {
                    const script = document.createElement('script');
                    script.src = 'https://unpkg.com/axe-core@4.7.0/axe.min.js';
                    document.head.appendChild(script);
                }
            """)

            # Wait for axe to load
            await page.wait_for_function("typeof window.axe !== 'undefined'", timeout=5000)

            # Run accessibility scan
            results = await page.evaluate("""
                new Promise((resolve) => {
                    axe.run({
                        tags: ['wcag2a', 'wcag2aa', 'wcag21aa']
                    }, (err, results) => {
                        if (err) {
                            resolve({ error: err.message });
                        } else {
                            resolve({
                                violations: results.violations.map(v => ({
                                    id: v.id,
                                    impact: v.impact,
                                    description: v.description,
                                    help: v.help,
                                    helpUrl: v.helpUrl,
                                    tags: v.tags,
                                    nodes: v.nodes.length
                                })),
                                passes: results.passes.length,
                                incomplete: results.incomplete.length,
                                inapplicable: results.inapplicable.length
                            });
                        }
                    });
                })
            """)

            if 'error' not in results:
                scan_result = {
                    'context': context_name,
                    'timestamp': time.time(),
                    'violations': results['violations'],
                    'summary': {
                        'total_violations': len(results['violations']),
                        'passes': results['passes'],
                        'incomplete': results['incomplete'],
                        'inapplicable': results['inapplicable']
                    }
                }

                self.accessibility_results.append(scan_result)
                print(f"✅ Accessibility scan complete - {len(results['violations'])} violations found")
            else:
                print(f"❌ Accessibility scan failed: {results['error']}")

        except Exception as e:
            print(f"❌ Error running accessibility scan: {e}")

    async def test_keyboard_navigation(self, page, context_name: str):
        """Test keyboard navigation coverage"""
        print(f"⌨️ Testing keyboard navigation for: {context_name}")

        try:
            # Get all interactive elements
            interactive_elements = await page.evaluate("""
                Array.from(document.querySelectorAll(
                    'button, input, select, textarea, a[href], [tabindex]:not([tabindex="-1"])'
                )).map(el => ({
                    tagName: el.tagName,
                    type: el.type || null,
                    id: el.id || null,
                    className: el.className || null,
                    tabIndex: el.tabIndex,
                    visible: el.offsetParent !== null
                }))
            """)

            visible_elements = [el for el in interactive_elements if el['visible']]
            expected_count = len(visible_elements)

            # Test tab navigation
            focus_order = []
            current_element = None

            for i in range(expected_count + 5):  # Extra tabs to detect issues
                await page.keyboard.press('Tab')

                current_element = await page.evaluate("""
                    {
                        tagName: document.activeElement.tagName,
                        id: document.activeElement.id || null,
                        className: document.activeElement.className || null,
                        isBody: document.activeElement === document.body
                    }
                """)

                focus_order.append(current_element)

                if current_element['isBody']:
                    break  # Reached end of tab cycle

            # Calculate coverage
            focused_elements = [f for f in focus_order if not f['isBody']]
            coverage_percentage = (len(set(str(f) for f in focused_elements)) / expected_count * 100) if expected_count > 0 else 0

            nav_result = {
                'context': context_name,
                'timestamp': time.time(),
                'expected_elements': expected_count,
                'focused_elements': len(focused_elements),
                'coverage_percentage': coverage_percentage,
                'focus_order': focus_order[:10],  # Limit to first 10 for brevity
                'interactive_elements': visible_elements
            }

            self.keyboard_nav_data.append(nav_result)
            print(f"✅ Keyboard navigation test complete - {coverage_percentage:.1f}% coverage")

        except Exception as e:
            print(f"❌ Error testing keyboard navigation: {e}")

    async def capture_contextual_screenshot(self, page, context_name: str, action_description: str):
        """Capture screenshot with context for UX analysis"""
        print(f"📸 Capturing contextual screenshot: {context_name}")

        try:
            screenshot_data = await page.screenshot(full_page=True)
            screenshot_base64 = base64.b64encode(screenshot_data).decode()

            screenshot_context = {
                'context': context_name,
                'action': action_description,
                'timestamp': time.time(),
                'screenshot_base64': screenshot_base64,
                'url': page.url,
                'title': await page.title()
            }

            self.screenshots_with_context.append(screenshot_context)
            print(f"✅ Screenshot captured for {context_name}")

        except Exception as e:
            print(f"❌ Error capturing screenshot: {e}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics summary"""
        if not self.performance_log:
            return {"error": "No performance data collected"}

        latencies = [m.action_latency for m in self.performance_log if m.action_latency]
        lcps = [m.lcp for m in self.performance_log if m.lcp]
        ttfbs = [m.ttfb for m in self.performance_log if m.ttfb]
        clss = [m.cls for m in self.performance_log if m.cls]

        return {
            "total_actions": len(self.performance_log),
            "action_latency": {
                "avg": sum(latencies) / len(latencies) if latencies else 0,
                "min": min(latencies) if latencies else 0,
                "max": max(latencies) if latencies else 0,
                "p95": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
            },
            "core_web_vitals": {
                "lcp_avg": sum(lcps) / len(lcps) if lcps else None,
                "ttfb_avg": sum(ttfbs) / len(ttfbs) if ttfbs else None,
                "cls_total": sum(clss) if clss else None
            },
            "raw_metrics": [asdict(m) for m in self.performance_log]
        }
