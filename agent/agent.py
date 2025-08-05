from computers import Computer
from utils import (
    create_response,
    show_image,
    pp,
    sanitize_message,
    check_blocklisted_url,
)
import json
from typing import Callable


class Agent:
    """
    A sample agent class that can be used to interact with a computer.

    (See simple_cua_loop.py for a simple example without an agent.)
    """

    def __init__(
        self,
        model="computer-use-preview",
        computer: Computer = None,
        tools: list[dict] = [],
        acknowledge_safety_check_callback: Callable = lambda: False,
    ):
        self.model = model
        self.computer = computer
        self.tools = tools
        self.print_steps = True
        self.debug = False
        self.show_images = False
        self.acknowledge_safety_check_callback = acknowledge_safety_check_callback

        if computer:
            dimensions = computer.get_dimensions()
            self.tools += [
                {
                    "type": "computer_20241022",
                    "display_width": dimensions[0],
                    "display_height": dimensions[1],
                    "environment": computer.get_environment(),
                },
            ]

    def debug_print(self, *args):
        if self.debug:
            pp(*args)

    def handle_item(self, item):
        """Handle each item; may cause a computer action + screenshot."""
        if item["type"] == "message":
            if self.print_steps:
                print(item["content"][0]["text"])

        if item["type"] == "function_call":
            name, args = item["name"], json.loads(item["arguments"])
            if self.print_steps:
                print(f"{name}({args})")

            if hasattr(self.computer, name):  # if function exists on computer, call it
                method = getattr(self.computer, name)
                method(**args)
            return [
                {
                    "type": "function_call_output",
                    "call_id": item["call_id"],
                    "output": "success",  # hard-coded output for demo
                }
            ]

        if item["type"] == "computer_call":
            action = item["action"]
            action_type = action["type"]
            action_args = {k: v for k, v in action.items() if k != "type"}
            if self.print_steps:
                print(f"{action_type}({action_args})")

            method = getattr(self.computer, action_type)
            method(**action_args)

            screenshot_base64 = self.computer.screenshot()
            if self.show_images:
                show_image(screenshot_base64)

            # if user doesn't ack all safety checks exit with error
            pending_checks = item.get("pending_safety_checks", [])
            for check in pending_checks:
                message = check["message"]
                if not self.acknowledge_safety_check_callback(message):
                    raise ValueError(
                        f"Safety check failed: {message}. Cannot continue with unacknowledged safety checks."
                    )

            call_output = {
                "type": "computer_call_output",
                "call_id": item["call_id"],
                "acknowledged_safety_checks": pending_checks,
                "output": {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"},
                },
            }

            # additional URL safety checks for browser environments
            if self.computer.get_environment() == "browser":
                current_url = self.computer.get_current_url()
                check_blocklisted_url(current_url)
                call_output["output"]["current_url"] = current_url

            return [call_output]
        return []

    def run_full_turn(
        self, input_items, print_steps=True, debug=False, show_images=False
    ):
        self.print_steps = print_steps
        self.debug = debug
        self.show_images = show_images
        new_items = []

        # keep looping until we get a final response
        while new_items[-1].get("role") != "assistant" if new_items else True:
            self.debug_print([sanitize_message(msg) for msg in input_items + new_items])

            response = create_response(
                model=self.model,
                input=input_items + new_items,
                tools=self.tools,
                truncation="auto",
            )
            
            # Debug logging (can be removed in production)
            if self.debug:
                print("DEBUG create_response returned:", response, flush=True)
                print("DEBUG response keys:", list(response.keys()) if isinstance(response, dict) else "Not a dict", flush=True)
            
            self.debug_print(response)

            # Handle error responses first
            if "error" in response:
                error_msg = response["error"].get("message", "Unknown API error")
                raise ValueError(f"API Error: {error_msg}")

            # Handle successful responses with different possible structures
            if "output" in response:
                new_items += response["output"]
                # Only call handle_item for non-assistant messages (e.g., function calls)
                for item in response["output"]:
                    if item.get("role") != "assistant":
                        new_items += self.handle_item(item)
            elif "items" in response:
                new_items += response["items"]
                for item in response["items"]:
                    if item.get("role") != "assistant":
                        new_items += self.handle_item(item)
            elif "choices" in response:
                # Handle direct OpenAI API response format
                choices = response["choices"]
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    if message:
                        new_items.append({
                            "role": "assistant",
                            "content": [{"type": "text", "text": message.get("content", "")}]
                        })
            elif isinstance(response, list):
                # Direct list response
                new_items += response
                for item in response:
                    if item.get("role") != "assistant":
                        new_items += self.handle_item(item)
            else:
                if self.debug:
                    print("DEBUG: Unexpected response structure:", response)
                    raise ValueError(f"Unknown response structure. Keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
                else:
                    # Fallback: try to extract any list from the response
                    extracted_items = []
                    if isinstance(response, dict):
                        for key, value in response.items():
                            if isinstance(value, list):
                                extracted_items = value
                                break
                    
                    if extracted_items:
                        new_items += extracted_items
                        for item in extracted_items:
                            if item.get("role") != "assistant":
                                new_items += self.handle_item(item)
                    else:
                        raise ValueError(f"No output found in response. Available keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")

        return new_items
