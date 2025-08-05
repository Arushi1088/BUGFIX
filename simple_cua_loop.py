from computers import Computer
from utils import create_response, check_blocklisted_url


def run_agent_noninteractive(
    screenshot_path: str,
    prompt: str,
    model: str = "computer-use-preview",
    computer: str = "local-playwright",
    width: int = 1920,
    height: int = 1080
) -> dict:
    from computers import Computer
    # 1) spin up the browser/computer
    comp = Computer.from_name(
        computer,
        display_width=width,
        display_height=height
    )
    # 2) feed it the screenshot + prompt
    response = comp.run(
        model=model,
        initial_screenshot=screenshot_path,
        user_input=prompt
    )
    return response


def acknowledge_safety_check_callback(message: str) -> bool:
    response = input(
        f"Safety Check Warning: {message}\nDo you want to acknowledge and proceed? (y/n): "
    ).lower()
    return response.strip() == "y"


def handle_item(item, computer):
    """Handle each item; may cause a computer action + screenshot."""
    if item["type"] == "message":  # print messages
        print(item["content"][0]["text"])

    if item["type"] == "computer_call":  # perform computer actions
        action = item["action"]
        action_type = action["type"]
        action_args = {k: v for k, v in action.items() if k != "type"}
        print(f"{action_type}({action_args})")

        # Computer operations are handled by the CUA CLI via tools parameter
        # No need to manually perform actions or take screenshots

        pending_checks = item.get("pending_safety_checks", [])
        for check in pending_checks:
            if not acknowledge_safety_check_callback(check["message"]):
                raise ValueError(f"Safety check failed: {check['message']}")

        # Return acknowledgment of safety checks if any
        if pending_checks:
            call_output = {
                "type": "computer_call_output",
                "call_id": item["call_id"],
                "acknowledged_safety_checks": pending_checks,
            }
            return [call_output]

    return []


def main():
    """Run the CUA (Computer Use Assistant) loop, using Local Playwright."""
    tools = [
        {
            "type": "computer_use_preview",
            "computer": "local-playwright",
            "display_width": 1920,
            "display_height": 1080
        }
    ]

    items = []
    while True:  # get user input forever
        user_input = input("> ")
        items.append({"role": "user", "content": user_input})

        while True:  # keep looping until we get a final response
            response = create_response(
                model="computer-use-preview",
                input=items,
                tools=tools,
                truncation="auto",
            )

            if "output" not in response:
                print(response)
                raise ValueError("No output from model")

            items += response["output"]

            for item in response["output"]:
                items += handle_item(item, None)  # No computer object needed

            if items[-1].get("role") == "assistant":
                break


if __name__ == "__main__":
    main()
