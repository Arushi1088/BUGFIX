import os
import sys
import json
import base64
import openai
import unicodedata

# Load environment variables if not already set
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

# Load your checklist JSON
with open("uiux_checklist.json") as f:
    CHECKLIST = json.load(f)

def format_checklist(checklist):
    lines = []
    for category, items in checklist.items():
        lines.append(f"## {category}")
        for it in items:
            lines.append(f"- {it}")
    return "\n".join(lines)

def build_prompt():
    # Build the raw prompt with checklist
    raw_prompt = f"""
You are a UX expert. Analyze the supplied screenshot using this checklist:
{format_checklist(CHECKLIST)}

Return a JSON array of issues, where each issue has:
- category: which checklist section
- item: the specific checklist item
- description: what's wrong
- (optional) bbox: [x, y, width, height]
Respond only with valid JSON.
"""
    
    # 1) Normalize Unicode (NFKC turns fancy dashes into normal ones, etc.)
    norm = unicodedata.normalize("NFKC", raw_prompt)
    
    # 2) Strip any remaining non-ASCII by replacing them
    ascii_only = norm.encode("ascii", errors="ignore").decode("ascii")
    
    # 3) Return the cleaned up prompt
    return ascii_only

def analyze_screenshot_simple(screenshot_path: str, custom_prompt: str = None):
    """Simple version using OpenAI's vision API directly."""
    client = openai.OpenAI()
    
    # Use custom prompt if provided, otherwise build default
    prompt_text = custom_prompt if custom_prompt else build_prompt()
    
    # Read and encode the screenshot
    with open(screenshot_path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        # Extract the response text
        assistant_text = response.choices[0].message.content
        
        # Try to parse as JSON, handling markdown code blocks
        try:
            # Remove markdown code blocks if present
            if "```json" in assistant_text:
                start = assistant_text.find("```json") + 7
                end = assistant_text.find("```", start)
                assistant_text = assistant_text[start:end].strip()
            elif "```" in assistant_text:
                start = assistant_text.find("```") + 3
                end = assistant_text.find("```", start)
                assistant_text = assistant_text[start:end].strip()
            
            issues = json.loads(assistant_text)
            return issues
        except json.JSONDecodeError as e:
            # If it's not valid JSON, wrap it in a simple structure
            return [{"category": "Analysis", "item": "Parse Error", "description": f"Could not parse JSON: {e}. Raw response: {assistant_text[:500]}..."}]
            
    except Exception as e:
        return [{"category": "Error", "item": "API Call Failed", "description": str(e)}]

def analyze_screenshot(path: str):
    issues = analyze_screenshot_simple(path)
    print(json.dumps(issues, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ux_analyzer_simple.py <screenshot.png>")
        sys.exit(1)
    analyze_screenshot(sys.argv[1])
