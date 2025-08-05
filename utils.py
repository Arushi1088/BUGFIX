import os
import requests
from dotenv import load_dotenv
import json
import base64
from PIL import Image
from io import BytesIO
import io
from urllib.parse import urlparse

load_dotenv(override=True)

BLOCKED_DOMAINS = [
    "maliciousbook.com",
    "evilvideos.com",
    "darkwebforum.com",
    "shadytok.com",
    "suspiciouspins.com",
    "ilanbigio.com",
]


def pp(obj):
    print(json.dumps(obj, indent=4))


def show_image(base_64_image):
    image_data = base64.b64decode(base_64_image)
    image = Image.open(BytesIO(image_data))
    image.show()


def calculate_image_dimensions(base_64_image):
    image_data = base64.b64decode(base_64_image)
    image = Image.open(io.BytesIO(image_data))
    return image.size


def sanitize_message(msg: dict) -> dict:
    """Return a copy of the message with image_url omitted for computer_call_output messages."""
    if msg.get("type") == "computer_call_output":
        output = msg.get("output", {})
        if isinstance(output, dict):
            sanitized = msg.copy()
            sanitized["output"] = {**output, "image_url": "[omitted]"}
            return sanitized
    return msg


def sanitize_payload(payload):
    """Sanitize Unicode characters in the JSON payload."""
    if isinstance(payload, dict):
        return {k: sanitize_payload(v) for k, v in payload.items()}
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    elif isinstance(payload, str):
        # Normalize and sanitize Unicode characters
        import unicodedata
        # First normalize to NFKC
        normalized = unicodedata.normalize("NFKC", payload)
        # Replace problematic Unicode characters
        sanitized = normalized.replace("\u2011", "-")  # non-breaking hyphen
        sanitized = sanitized.replace("\u2012", "-")   # figure dash  
        sanitized = sanitized.replace("\u2013", "-")   # en dash
        sanitized = sanitized.replace("\u2014", "-")   # em dash
        sanitized = sanitized.replace("\u2015", "-")   # horizontal bar
        sanitized = sanitized.replace("\u2010", "-")   # hyphen
        sanitized = sanitized.replace("\u00a0", " ")   # non-breaking space
        sanitized = sanitized.replace("\u202f", " ")   # narrow no-break space
        sanitized = sanitized.replace("\u2009", " ")   # thin space
        
        # Encode to UTF-8 and decode back to remove any remaining issues
        try:
            return sanitized.encode('utf-8', errors='ignore').decode('utf-8')
        except UnicodeError:
            return sanitized.encode('ascii', errors='ignore').decode('ascii')
    else:
        return payload


def create_response(**kwargs):
    url = "https://api.openai.com/v1/chat/completions"
    
    # Start with basic headers that are guaranteed to be ASCII/Latin-1 safe
    headers = {
        "Content-Type": "application/json"
    }

    # Safely handle API key - clean any Unicode before putting in header
    api_key = os.getenv('OPENAI_API_KEY', '')
    if api_key:
        # Replace Unicode hyphens with regular ASCII hyphens to preserve key validity
        clean_api_key = api_key.replace('\u2011', '-')  # non-breaking hyphen
        clean_api_key = clean_api_key.replace('\u2012', '-')  # figure dash
        clean_api_key = clean_api_key.replace('\u2013', '-')  # en dash
        clean_api_key = clean_api_key.replace('\u2014', '-')  # em dash
        clean_api_key = clean_api_key.replace('\u2015', '-')  # horizontal bar
        clean_api_key = clean_api_key.replace('\u2010', '-')  # hyphen
        clean_api_key = clean_api_key.replace('\u00a0', ' ')  # non-breaking space
        clean_api_key = clean_api_key.replace('\u202f', ' ')  # narrow no-break space
        clean_api_key = clean_api_key.replace('\u2009', ' ')  # thin space
        
        # Remove any remaining non-ASCII characters to ensure header safety
        # Use a more conservative approach that only keeps ASCII characters
        clean_api_key = ''.join(c for c in clean_api_key if ord(c) < 128)
            
        headers["Authorization"] = f"Bearer {clean_api_key}"

    # Handle organization ID safely
    openai_org = os.getenv("OPENAI_ORG")
    if openai_org:
        # Clean organization ID too - only keep ASCII characters
        clean_org = ''.join(c for c in openai_org if ord(c) < 128)
        headers["Openai-Organization"] = clean_org

    # Debug: Verify all headers are now ASCII/Latin-1 safe
    print("→ REQUEST HEADERS (cleaned):")
    for name, value in headers.items():
        print(f"  {name!r}: {value!r}")
        try:
            value.encode('latin-1')
            print(f"    ✅ {name} is latin-1 safe")
        except UnicodeEncodeError as e:
            print(f"    ❌ {name} still has issue: {e}")
    
    # Transform kwargs to proper OpenAI API format
    # Expecting: model, input (messages), tools, truncation
    payload = {
        "model": kwargs.get("model", "gpt-4o"),
        "messages": kwargs.get("input", []),
        "max_tokens": kwargs.get("max_tokens", 2000)
    }
    
    # Add tools if provided
    if "tools" in kwargs and kwargs["tools"]:
        payload["tools"] = kwargs["tools"]
    
    # Sanitize the JSON payload (Unicode is OK in JSON body)
    safe_payload = sanitize_payload(payload)
    print(f"📦 Payload sanitized, keys: {list(safe_payload.keys()) if isinstance(safe_payload, dict) else 'non-dict'}")
    
    # Handle placeholder API key - simulate successful response for testing
    if clean_api_key == "sk-YOUR_KEY_HERE":
        print("🧪 Using placeholder API key - simulating successful response for testing")
        simulated_response = {
            "output": [{
                "role": "assistant",
                "content": [{
                    "type": "text", 
                    "text": '''[
                        {
                            "category": "Visual Design",
                            "item": "Typography readability", 
                            "description": "The text appears clear and readable with good contrast",
                            "severity": "low"
                        },
                        {
                            "category": "Navigation",
                            "item": "Clear navigation structure",
                            "description": "Simple navigation structure is present",
                            "severity": "low"
                        }
                    ]'''
                }]
            }]
        }
        return simulated_response
    
    response = requests.post(url, headers=headers, json=safe_payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
        return response.json()  # Return error response as-is
    
    # Transform OpenAI response to expected format
    openai_response = response.json()
    
    # Convert from OpenAI format to expected agent format
    if "choices" in openai_response and openai_response["choices"]:
        choice = openai_response["choices"][0]
        message = choice.get("message", {})
        
        # Return in expected format with "output" key containing list of messages
        return {
            "output": [{
                "role": "assistant",
                "content": [{"type": "text", "text": message.get("content", "")}]
            }]
        }
    else:
        return {"error": {"message": "No valid response from OpenAI API"}}


def check_blocklisted_url(url: str) -> None:
    """Raise ValueError if the given URL (including subdomains) is in the blocklist."""
    hostname = urlparse(url).hostname or ""
    if any(
        hostname == blocked or hostname.endswith(f".{blocked}")
        for blocked in BLOCKED_DOMAINS
    ):
        raise ValueError(f"Blocked URL: {url}")


def plan_actions(scenario: str) -> list:
    """
    Smart AI planner that prioritizes staying on current site and using site-specific functionality.
    Returns a list of actions to perform based on the scenario.
    """
    print(f"🤖 AI Planning for scenario: {scenario}")
    
    # Enhanced prompt to prioritize site-specific search over Google navigation
    planning_prompt = f"""
You are a smart web automation planner. Given a user scenario, create a step-by-step action plan.

IMPORTANT GUIDELINES:
1. If the scenario involves searching for something, PRIORITIZE using the current website's search functionality
2. Only navigate to Google as an ABSOLUTE LAST RESORT if no search exists on the current site
3. Always try to stay on the current website when possible
4. Look for site-specific search boxes, navigation, filters, etc. before going external

SCENARIO: {scenario}

Current context: User is already on a website and wants to accomplish a task.

Return a JSON array of actions. Each action should have:
- "action": one of ["goto", "click", "fill", "press", "wait"]
- "selector": CSS selector (for click/fill/wait actions)
- "value": value to use (for goto/fill/press actions)

Example response for "search for dress":
[
    {{"action": "fill", "selector": "input[type='search'], input[placeholder*='search'], input[name*='search']", "value": "dress"}},
    {{"action": "press", "selector": "", "value": "Enter"}}
]

Only use "goto" to Google if absolutely no search functionality exists on the current site.
Prioritize finding and using the website's own search, navigation, and filtering capabilities.

Return only the JSON array, no other text.
"""

    try:
        # Use our create_response function to call OpenAI
        response = create_response(
            model="gpt-4o",
            input=[{"role": "user", "content": planning_prompt}],
            max_tokens=1000
        )
        
        if "output" in response and response["output"]:
            content = response["output"][0]["content"][0]["text"]
            
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                actions_json = json_match.group(0)
                actions = json.loads(actions_json)
                print(f"📋 Generated {len(actions)} smart actions (prioritizing current site)")
                return actions
            else:
                print("⚠️ Could not extract JSON from AI response")
                
    except Exception as e:
        print(f"⚠️ AI planning failed: {e}")
    
    # Fallback: simple actions based on common patterns
    if "search" in scenario.lower():
        query_match = re.search(r'search.*?["\']([^"\']+)["\']|search.*?for\s+([^\s]+)', scenario, re.IGNORECASE)
        if query_match:
            query = query_match.group(1) or query_match.group(2)
            print(f"🔄 Fallback plan: search for '{query}' on current site")
            return [
                {"action": "fill", "selector": "input[type='search'], input[placeholder*='search'], input[name*='search'], #search", "value": query},
                {"action": "press", "selector": "", "value": "Enter"}
            ]
    
    print("🔄 Fallback plan: no specific actions")
    return []


def run_ux_audit(image_data):
    """
    Perform UX audit on screenshot or page content.
    Takes image bytes and returns UX analysis.
    """
    print("📊 Running UX audit...")
    
    try:
        # Convert image bytes to base64 for API
        if isinstance(image_data, bytes):
            # It's image data
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            content_type = "image"
        else:
            # It's text content
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            content_type = "text"
        
        audit_prompt = """
Analyze this webpage screenshot/content for UX issues. Focus on:

1. **Visual Design**: Typography, colors, contrast, spacing, alignment
2. **Navigation**: Menu clarity, breadcrumbs, search functionality
3. **Content**: Readability, hierarchy, calls-to-action
4. **Layout**: Responsive design, white space usage, grid alignment
5. **Accessibility**: Color contrast, text size, button clarity
6. **User Flow**: Ease of finding information, conversion paths

Return a JSON array of findings. Each finding should have:
- "category": one of the categories above
- "item": brief title of the issue/observation
- "description": detailed explanation
- "severity": "low", "medium", or "high"

Focus on actionable insights that would improve user experience.
Return only the JSON array, no other text.
"""

        if content_type == "image":
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": audit_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
        else:
            messages = [
                {
                    "role": "user", 
                    "content": f"{audit_prompt}\n\nPage content to analyze:\n{image_data.decode('utf-8', errors='ignore')[:3000]}..."
                }
            ]
        
        response = create_response(
            model="gpt-4o",
            input=messages,
            max_tokens=2000
        )
        
        if "output" in response and response["output"]:
            content = response["output"][0]["content"][0]["text"]
            
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                audit_json = json_match.group(0)
                audit_results = json.loads(audit_json)
                print(f"✅ UX audit complete: {len(audit_results)} findings")
                return {
                    "status": "success",
                    "findings": audit_results,
                    "summary": f"Found {len(audit_results)} UX observations"
                }
            else:
                print("⚠️ Could not extract JSON from audit response")
                return {
                    "status": "partial",
                    "findings": [],
                    "summary": "AI response received but could not parse results",
                    "raw_response": content[:500]
                }
                
    except Exception as e:
        print(f"❌ UX audit failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "findings": [],
            "summary": "UX audit failed due to technical error"
        }
