#!/usr/bin/env python3
"""
🔧 Browser Action Tools for UX Analyzer
Playwright-powered functions that can be called by GPT-4o for interactive testing.
"""

import json
import time
from typing import Optional, Dict, Any
from playwright.sync_api import Page, Browser, TimeoutError as PlaywrightTimeoutError

class BrowserTools:
    """Browser automation tools that can be called by AI agents."""
    
    def __init__(self, page: Page):
        self.page = page
        self.last_action_result = None
    
    def goto(self, url: str) -> Dict[str, Any]:
        """Navigate the browser to the given URL."""
        try:
            print(f"🌐 Navigating to: {url}")
            self.page.goto(url, wait_until="load", timeout=5000)
            current_url = self.page.url
            title = self.page.title()
            
            result = {
                "success": True,
                "action": "goto",
                "url": current_url,
                "title": title,
                "message": f"Successfully navigated to {current_url}"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "goto",
                "error": str(e),
                "message": f"Failed to navigate to {url}: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def click(self, selector: str, description: str = "") -> Dict[str, Any]:
        """Click on the element matching the CSS selector with automatic disambiguation."""
        try:
            print(f"🖱️ Clicking: {selector} ({description})")
            
            # Try clicking with disambiguation
            return self._click_with_disambiguation(selector, description)
            
        except Exception as e:
            result = {
                "success": False,
                "action": "click",
                "selector": selector,
                "description": description,
                "error": str(e),
                "message": f"Failed to click {selector}: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def _click_with_disambiguation(self, selector: str, description: str) -> Dict[str, Any]:
        """Click with automatic disambiguation for multiple matches."""
        try:
            # Wait for element to be visible
            self.page.wait_for_selector(selector, timeout=5000)
            
            # Check if selector matches multiple elements
            elements = self.page.locator(selector)
            count = elements.count()
            
            if count == 0:
                raise Exception(f"No elements found matching selector: {selector}")
            elif count == 1:
                # Single match - proceed normally
                elements.scroll_into_view_if_needed()
                elements.click()
                time.sleep(0.5)
                
                result = {
                    "success": True,
                    "action": "click",
                    "selector": selector,
                    "description": description,
                    "message": f"Successfully clicked {selector}"
                }
            else:
                # Multiple matches - use disambiguation
                print(f"⚠️ Multiple elements ({count}) found for selector: {selector}")
                
                # Try different disambiguation strategies
                disambiguated_selector = self._disambiguate_selector(selector, description, count)
                
                if disambiguated_selector:
                    print(f"🔧 Using disambiguated selector: {disambiguated_selector}")
                    
                    # Try clicking the disambiguated selector
                    disambiguated_element = self.page.locator(disambiguated_selector)
                    disambiguated_element.scroll_into_view_if_needed()
                    disambiguated_element.click()
                    time.sleep(0.5)
                    
                    result = {
                        "success": True,
                        "action": "click",
                        "selector": selector,
                        "disambiguated_selector": disambiguated_selector,
                        "description": description,
                        "matches_found": count,
                        "message": f"Successfully clicked {disambiguated_selector} (disambiguated from {selector})"
                    }
                else:
                    # Fall back to first element
                    print(f"🎯 Falling back to first element")
                    first_element = elements.first()
                    first_element.scroll_into_view_if_needed()
                    first_element.click()
                    time.sleep(0.5)
                    
                    result = {
                        "success": True,
                        "action": "click",
                        "selector": selector,
                        "disambiguated_selector": f"{selector}:first-child",
                        "description": description,
                        "matches_found": count,
                        "message": f"Successfully clicked first of {count} matches for {selector}"
                    }
            
            self.last_action_result = result
            return result
            
        except PlaywrightTimeoutError:
            result = {
                "success": False,
                "action": "click",
                "selector": selector,
                "error": "Element not found or not clickable",
                "message": f"Could not find clickable element: {selector}"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "click",
                "selector": selector,
                "error": str(e),
                "message": f"Failed to click {selector}: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def _disambiguate_selector(self, selector: str, description: str, count: int) -> Optional[str]:
        """
        Try to disambiguate a selector that matches multiple elements.
        
        Args:
            selector: Original CSS selector
            description: Human description of what we're looking for
            count: Number of matches found
            
        Returns:
            Refined selector or None if no good disambiguation found
        """
        # Strategy 1: If description mentions specific text, try text-based selectors
        if description and any(word in description.lower() for word in ['contact', 'us', 'submit', 'send', 'save']):
            # Try more specific text matching
            for text_hint in ['contact us', 'contact', 'submit', 'send', 'save']:
                if text_hint in description.lower():
                    text_selector = f"{selector}:has-text('{text_hint}')"
                    try:
                        if self.page.locator(text_selector).count() == 1:
                            return text_selector
                    except:
                        pass
        
        # Strategy 2: Try visible elements only
        visible_selector = f"{selector}:visible"
        try:
            visible_count = self.page.locator(visible_selector).count()
            if visible_count == 1:
                return visible_selector
            elif visible_count < count:  # Reduced the options
                return visible_selector
        except:
            pass
        
        # Strategy 3: Try first element that's not disabled
        enabled_selector = f"{selector}:not([disabled])"
        try:
            enabled_count = self.page.locator(enabled_selector).count()
            if enabled_count == 1:
                return enabled_selector
            elif enabled_count < count:
                return enabled_selector
        except:
            pass
        
        # Strategy 4: Try elements with specific roles
        if 'button' in selector.lower():
            button_role_selector = f"{selector}[role='button']"
            try:
                if self.page.locator(button_role_selector).count() == 1:
                    return button_role_selector
            except:
                pass
        
        # Strategy 5: For common patterns, try nth-child
        if count <= 3:  # Don't use nth-child for too many elements
            # Try the first element (most common case)
            return f"{selector}:nth-child(1)"
        
        return None
    
    def fill(self, selector: str, text: str, description: str = "") -> Dict[str, Any]:
        """Type text into the element matching the CSS selector."""
        try:
            print(f"⌨️ Filling: {selector} with '{text}' ({description})")
            
            # Wait for element
            self.page.wait_for_selector(selector, timeout=5000)
            
            # Clear and fill
            self.page.fill(selector, text)
            
            result = {
                "success": True,
                "action": "fill",
                "selector": selector,
                "text": text,
                "description": description,
                "message": f"Successfully filled {selector} with text"
            }
            self.last_action_result = result
            return result
            
        except PlaywrightTimeoutError:
            result = {
                "success": False,
                "action": "fill",
                "selector": selector,
                "error": "Element not found",
                "message": f"Could not find input element: {selector}"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "fill",
                "selector": selector,
                "error": str(e),
                "message": f"Failed to fill {selector}: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def wait_for_element(self, selector: str, timeout: int = 5000) -> Dict[str, Any]:
        """Wait until the selector appears (or timeout)."""
        try:
            print(f"⏳ Waiting for: {selector}")
            self.page.wait_for_selector(selector, timeout=timeout)
            
            result = {
                "success": True,
                "action": "wait_for_element",
                "selector": selector,
                "message": f"Element {selector} appeared successfully"
            }
            self.last_action_result = result
            return result
            
        except PlaywrightTimeoutError:
            result = {
                "success": False,
                "action": "wait_for_element",
                "selector": selector,
                "error": "Timeout waiting for element",
                "message": f"Element {selector} did not appear within {timeout}ms"
            }
            self.last_action_result = result
            return result
    
    def scroll_to(self, selector: str) -> Dict[str, Any]:
        """Scroll to the element matching the CSS selector."""
        try:
            print(f"📜 Scrolling to: {selector}")
            self.page.locator(selector).scroll_into_view_if_needed()
            time.sleep(0.3)  # Brief pause after scrolling
            
            result = {
                "success": True,
                "action": "scroll_to",
                "selector": selector,
                "message": f"Successfully scrolled to {selector}"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "scroll_to",
                "selector": selector,
                "error": str(e),
                "message": f"Failed to scroll to {selector}: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def screenshot(self) -> Dict[str, Any]:
        """Take a screenshot and return its base64 data."""
        try:
            print("📸 Taking screenshot...")
            screenshot_bytes = self.page.screenshot(full_page=False)
            
            import base64
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            result = {
                "success": True,
                "action": "screenshot",
                "screenshot_data": screenshot_b64,
                "size": len(screenshot_bytes),
                "message": "Screenshot captured successfully"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "screenshot",
                "error": str(e),
                "message": f"Failed to take screenshot: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def get_page_info(self) -> Dict[str, Any]:
        """Get current page information (URL, title, etc.)."""
        try:
            result = {
                "success": True,
                "action": "get_page_info",
                "url": self.page.url,
                "title": self.page.title(),
                "message": "Page info retrieved successfully"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "get_page_info", 
                "error": str(e),
                "message": f"Failed to get page info: {str(e)}"
            }
            self.last_action_result = result
            return result
    
    def find_elements(self, description: str) -> Dict[str, Any]:
        """Find elements on the page based on description."""
        try:
            print(f"🔍 Looking for elements: {description}")
            
            # Common selectors to try based on description
            selectors_to_try = []
            desc_lower = description.lower()
            
            if "button" in desc_lower:
                selectors_to_try.extend([
                    "button",
                    "input[type='button']",
                    "input[type='submit']",
                    "[role='button']",
                    "a.btn",
                    ".button"
                ])
            
            if "link" in desc_lower:
                selectors_to_try.extend(["a", "a[href]"])
            
            if "input" in desc_lower or "text" in desc_lower:
                selectors_to_try.extend([
                    "input[type='text']",
                    "input[type='search']",
                    "input:not([type])",
                    "textarea"
                ])
            
            if "form" in desc_lower:
                selectors_to_try.extend(["form"])
            
            # Also try to find by text content
            for word in desc_lower.split():
                if len(word) > 3:  # Skip short words
                    selectors_to_try.append(f"text='{word}'")
                    selectors_to_try.append(f"*:has-text('{word}')")
            
            found_elements = []
            for selector in selectors_to_try[:10]:  # Limit to avoid too many queries
                try:
                    elements = self.page.locator(selector).all()
                    for i, element in enumerate(elements[:3]):  # Max 3 per selector
                        try:
                            if element.is_visible():
                                text_content = element.inner_text()[:50]
                                found_elements.append({
                                    "selector": selector,
                                    "index": i,
                                    "text": text_content,
                                    "visible": True
                                })
                        except:
                            pass
                except:
                    pass
            
            result = {
                "success": True,
                "action": "find_elements",
                "description": description,
                "found_elements": found_elements[:10],  # Limit results
                "message": f"Found {len(found_elements)} elements matching '{description}'"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "find_elements",
                "description": description,
                "error": str(e),
                "message": f"Failed to find elements: {str(e)}"
            }
            self.last_action_result = result
            return result

    def finish(self, analysis: str, task_completed: bool = True) -> Dict[str, Any]:
        """Signal that the UX testing scenario is complete and provide final analysis."""
        try:
            print(f"✅ Task completed: {task_completed}")
            print(f"📝 Final analysis: {analysis}")
            
            result = {
                "success": True,
                "action": "finish",
                "task_completed": task_completed,
                "analysis": analysis,
                "message": "UX testing scenario completed"
            }
            self.last_action_result = result
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "action": "finish",
                "error": str(e),
                "message": f"Error finishing task: {str(e)}"
            }
            self.last_action_result = result
            return result


# Function definitions for OpenAI function calling
BROWSER_FUNCTIONS = [
    {
        "name": "goto",
        "description": "Navigate the browser to a specific URL",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to navigate to"
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "click",
        "description": "Click on an element using CSS selector",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the element to click"
                },
                "description": {
                    "type": "string",
                    "description": "Human-readable description of what you're clicking"
                }
            },
            "required": ["selector"]
        }
    },
    {
        "name": "fill",
        "description": "Fill a form input with text",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the input element"
                },
                "text": {
                    "type": "string",
                    "description": "Text to type into the input"
                },
                "description": {
                    "type": "string",
                    "description": "Human-readable description of the input field"
                }
            },
            "required": ["selector", "text"]
        }
    },
    {
        "name": "wait_for_element",
        "description": "Wait for an element to appear on the page",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the element to wait for"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum time to wait in milliseconds",
                    "default": 5000
                }
            },
            "required": ["selector"]
        }
    },
    {
        "name": "screenshot",
        "description": "Take a screenshot of the current page",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_page_info",
        "description": "Get current page URL, title, and other basic info",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "find_elements",
        "description": "Find elements on the page based on a description",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Description of what you're looking for (e.g., 'search button', 'login form', 'contact link')"
                }
            },
            "required": ["description"]
        }
    },
    {
        "name": "scroll_to",
        "description": "Scroll to an element on the page",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the element to scroll to"
                }
            },
            "required": ["selector"]
        }
    },
    {
        "name": "finish",
        "description": "Signal that the UX testing scenario is complete and provide final analysis",
        "parameters": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "string",
                    "description": "Final analysis of the UX testing scenario - what was learned, issues found, task completion status"
                },
                "task_completed": {
                    "type": "boolean",
                    "description": "Whether the testing scenario was successfully completed",
                    "default": True
                }
            },
            "required": ["analysis"]
        }
    }
]
