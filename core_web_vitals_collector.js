
class CoreWebVitalsCollector {
    constructor() {
        this.metrics = {
            lcp: null,
            fid: null,
            cls: 0,
            ttfb: null,
            fcp: null,
            inp: null,  // Interaction to Next Paint
            clsEntries: [],
            performanceEntries: []
        };

        this.observers = [];
        this.setupObservers();
    }

    setupObservers() {
        // Largest Contentful Paint (LCP)
        if ('PerformanceObserver' in window) {
            const lcpObserver = new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.metrics.lcp = lastEntry.startTime;
                console.log(`📊 LCP: ${lastEntry.startTime.toFixed(2)}ms`);
            });

            try {
                lcpObserver.observe({entryTypes: ['largest-contentful-paint']});
                this.observers.push(lcpObserver);
            } catch (e) {
                console.warn('LCP observer not supported');
            }

            // First Input Delay (FID) & Interaction to Next Paint (INP)
            const fidObserver = new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (entry.name === 'first-input') {
                        this.metrics.fid = entry.processingStart - entry.startTime;
                        console.log(`📊 FID: ${this.metrics.fid.toFixed(2)}ms`);
                    }

                    // Track all interactions for INP calculation
                    if (entry.interactionId) {
                        const interactionTime = entry.processingStart - entry.startTime;
                        this.metrics.inp = Math.max(this.metrics.inp || 0, interactionTime);
                    }
                }
            });

            try {
                fidObserver.observe({entryTypes: ['first-input'], buffered: true});
                this.observers.push(fidObserver);
            } catch (e) {
                console.warn('FID observer not supported');
            }

            // Cumulative Layout Shift (CLS)
            const clsObserver = new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (!entry.hadRecentInput) {
                        this.metrics.clsEntries.push({
                            value: entry.value,
                            startTime: entry.startTime,
                            sources: entry.sources?.map(source => ({
                                node: source.node?.tagName || 'unknown',
                                previousRect: source.previousRect,
                                currentRect: source.currentRect
                            })) || []
                        });

                        this.metrics.cls += entry.value;
                        console.log(`📊 CLS: ${this.metrics.cls.toFixed(4)} (+${entry.value.toFixed(4)})`);
                    }
                }
            });

            try {
                clsObserver.observe({entryTypes: ['layout-shift']});
                this.observers.push(clsObserver);
            } catch (e) {
                console.warn('CLS observer not supported');
            }

            // First Contentful Paint (FCP)
            const paintObserver = new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (entry.name === 'first-contentful-paint') {
                        this.metrics.fcp = entry.startTime;
                        console.log(`📊 FCP: ${entry.startTime.toFixed(2)}ms`);
                    }
                }
            });

            try {
                paintObserver.observe({entryTypes: ['paint']});
                this.observers.push(paintObserver);
            } catch (e) {
                console.warn('Paint observer not supported');
            }
        }

        // Calculate TTFB from Navigation Timing
        this.calculateTTFB();
    }

    calculateTTFB() {
        if ('performance' in window && 'getEntriesByType' in performance) {
            const navigation = performance.getEntriesByType('navigation')[0];
            if (navigation) {
                this.metrics.ttfb = navigation.responseStart - navigation.requestStart;
                console.log(`📊 TTFB: ${this.metrics.ttfb.toFixed(2)}ms`);
            }
        }
    }

    getDetailedMetrics() {
        const navigation = performance.getEntriesByType('navigation')[0];
        const resources = performance.getEntriesByType('resource');

        return {
            // Core Web Vitals
            coreWebVitals: {
                lcp: this.metrics.lcp,
                fid: this.metrics.fid,
                cls: this.metrics.cls,
                fcp: this.metrics.fcp,
                inp: this.metrics.inp,
                ttfb: this.metrics.ttfb
            },

            // Detailed timing breakdown
            timingBreakdown: navigation ? {
                // Network timing
                redirectTime: navigation.redirectEnd - navigation.redirectStart,
                dnsTime: navigation.domainLookupEnd - navigation.domainLookupStart,
                tcpTime: navigation.connectEnd - navigation.connectStart,
                tlsTime: navigation.secureConnectionStart > 0 ? 
                    navigation.connectEnd - navigation.secureConnectionStart : 0,
                requestTime: navigation.responseStart - navigation.requestStart,
                responseTime: navigation.responseEnd - navigation.responseStart,

                // Processing timing
                domParseTime: navigation.domContentLoadedEventStart - navigation.responseEnd,
                domContentLoadedTime: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                loadEventTime: navigation.loadEventEnd - navigation.loadEventStart,

                // Total times
                totalTime: navigation.loadEventEnd - navigation.navigationStart,
                domInteractiveTime: navigation.domInteractive - navigation.navigationStart,
                domCompleteTime: navigation.domComplete - navigation.navigationStart
            } : null,

            // Resource timing summary
            resourceSummary: {
                totalResources: resources.length,
                imageResources: resources.filter(r => r.initiatorType === 'img').length,
                scriptResources: resources.filter(r => r.initiatorType === 'script').length,
                stylesheetResources: resources.filter(r => r.initiatorType === 'link').length,
                averageResourceTime: resources.length > 0 ? 
                    resources.reduce((sum, r) => sum + (r.responseEnd - r.startTime), 0) / resources.length : 0
            },

            // Memory information (if available)
            memory: performance.memory ? {
                usedJSHeapSize: performance.memory.usedJSHeapSize,
                totalJSHeapSize: performance.memory.totalJSHeapSize,
                jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
                usagePercentage: (performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) * 100
            } : null,

            // Layout shift details
            layoutShifts: this.metrics.clsEntries,

            // Performance score estimates (based on Lighthouse scoring)
            performanceScores: this.calculatePerformanceScores()
        };
    }

    calculatePerformanceScores() {
        // Simplified Lighthouse-style scoring
        const scores = {};

        // LCP scoring (0-2.5s = good, 2.5-4s = needs improvement, >4s = poor)
        if (this.metrics.lcp !== null) {
            if (this.metrics.lcp <= 2500) scores.lcp = 'good';
            else if (this.metrics.lcp <= 4000) scores.lcp = 'needs-improvement';
            else scores.lcp = 'poor';
        }

        // FID scoring (0-100ms = good, 100-300ms = needs improvement, >300ms = poor)
        if (this.metrics.fid !== null) {
            if (this.metrics.fid <= 100) scores.fid = 'good';
            else if (this.metrics.fid <= 300) scores.fid = 'needs-improvement';
            else scores.fid = 'poor';
        }

        // CLS scoring (0-0.1 = good, 0.1-0.25 = needs improvement, >0.25 = poor)
        if (this.metrics.cls <= 0.1) scores.cls = 'good';
        else if (this.metrics.cls <= 0.25) scores.cls = 'needs-improvement';
        else scores.cls = 'poor';

        // TTFB scoring (0-800ms = good, 800-1800ms = needs improvement, >1800ms = poor)
        if (this.metrics.ttfb !== null) {
            if (this.metrics.ttfb <= 800) scores.ttfb = 'good';
            else if (this.metrics.ttfb <= 1800) scores.ttfb = 'needs-improvement';
            else scores.ttfb = 'poor';
        }

        return scores;
    }

    generatePerformanceReport() {
        const metrics = this.getDetailedMetrics();

        console.group('📊 Core Web Vitals Report');
        console.log('LCP (Largest Contentful Paint):', metrics.coreWebVitals.lcp?.toFixed(2) + 'ms');
        console.log('FID (First Input Delay):', metrics.coreWebVitals.fid?.toFixed(2) + 'ms');
        console.log('CLS (Cumulative Layout Shift):', metrics.coreWebVitals.cls?.toFixed(4));
        console.log('FCP (First Contentful Paint):', metrics.coreWebVitals.fcp?.toFixed(2) + 'ms');
        console.log('TTFB (Time to First Byte):', metrics.coreWebVitals.ttfb?.toFixed(2) + 'ms');
        console.groupEnd();

        return metrics;
    }

    cleanup() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers = [];
    }
}

// Initialize global collector
if (!window.coreWebVitalsCollector) {
    window.coreWebVitalsCollector = new CoreWebVitalsCollector();
    console.log('🚀 Core Web Vitals monitoring initialized');
}

// Expose collection function
window.getAdvancedPerformanceMetrics = () => {
    return window.coreWebVitalsCollector.getDetailedMetrics();
};

window.generatePerformanceReport = () => {
    return window.coreWebVitalsCollector.generatePerformanceReport();
};
