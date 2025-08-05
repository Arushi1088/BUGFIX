import os
import sys
import json
import base64

# Load environment variables if not already set
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

# 1. Import the Playwright-based Computer and the Agent loop
from computers.default.local_playwright import LocalPlaywrightBrowser
from agent.agent import Agent

# 2. Load your checklist JSON (unchanged)
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
    return f"""
You are a UX expert. Analyze the supplied screenshot using this checklist:
{format_checklist(CHECKLIST)}

Return a JSON array of issues, where each issue has:
- category: which checklist section
- item: the specific checklist item
- description: what's wrong
- (optional) bbox: [x, y, width, height]
Respond only with valid JSON.
"""

def run_agent_noninteractive(screenshot_path: str, prompt: str):
    # 3. Spin up Playwright
    with LocalPlaywrightBrowser() as computer:
        # 4. Create the Agent
        agent = Agent(model="gpt-4o", computer=computer, tools=[])
        
        # 5. Read & embed the screenshot as base64
        with open(screenshot_path, "rb") as img:
            b64 = base64.b64encode(img.read()).decode()
        
        # 6. Build the user message with embedded image
        user_message = {
            "role": "user", 
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{b64}"
                },
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
        }
        
        # 7. Run exactly one "full turn"
        output_items = agent.run_full_turn(
            input_items=[user_message],
            print_steps=False,
            debug=False,
            show_images=False
        )

    # 8. Extract assistant text and parse JSON
    assistant_text = ""
    for it in output_items:
        if it.get("role") == "assistant":
            assistant_text += it["content"][0]["text"]
    return json.loads(assistant_text)

def analyze_screenshot(path: str):
    issues = run_agent_noninteractive(path, build_prompt())
    print(json.dumps(issues, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ux_analyzer.py <screenshot.png>")
        sys.exit(1)
    analyze_screenshot(sys.argv[1])
