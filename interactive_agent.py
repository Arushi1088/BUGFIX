#!/usr/bin/env python3
"""
🤖 Interactive UX Testing Agent
GPT-4o powered agent that can perform browser actions and analyze UX.
"""

import json
from typing import List, Dict, Any, Optional
from tools import BrowserTools, BROWSER_FUNCTIONS
from computers.default.local_playwright import LocalPlaywrightBrowser
from openai_client import OpenAIClientWrapper

class InteractiveUXAgent:
    """Agent that combines GPT-4o vision with browser automation for UX testing."""
    
    def __init__(self, 
                 model: str = "gpt-4o",
                 fallback_model: str = "gpt-3.5-turbo",
                 enable_fallback: bool = True):
        self.model = model
        self.fallback_model = fallback_model
        self.enable_fallback = enable_fallback
        self.client = OpenAIClientWrapper(
            primary_model=model,
            fallback_model=fallback_model
        )
        self.browser_tools = None
        self.conversation_history = []
        self.max_actions = 15  # Prevent infinite loops
    
    def _suggest_batch_optimizations(self, scenario: str) -> str:
        """Suggest logical batching strategies for the given scenario."""
        suggestions = []
        
        # Common batching patterns
        if any(keyword in scenario.lower() for keyword in ['find', 'locate', 'look for']):
            suggestions.append("Consider using find_elements first to locate targets, then take a screenshot to see the full context")
        
        if any(keyword in scenario.lower() for keyword in ['form', 'fill', 'enter', 'input']):
            suggestions.append("For forms: gather all field information, then fill multiple fields in sequence before taking a final screenshot")
        
        if any(keyword in scenario.lower() for keyword in ['navigate', 'click', 'go to']):
            suggestions.append("For navigation: click → wait_for_element → screenshot in sequence for efficient flow verification")
        
        if any(keyword in scenario.lower() for keyword in ['test', 'verify', 'check']):
            suggestions.append("For testing: screenshot → find_elements → perform actions → final screenshot for before/after comparison")
        
        return "\n".join(f"💡 {suggestion}" for suggestion in suggestions) if suggestions else ""
        
    def analyze_scenario(self, url: str, scenario: str) -> Dict[str, Any]:
        """
        Analyze a UX scenario by performing interactive testing using the interactive loop.
        
        The loop follows this protocol:
        1. System: "You're a UX-testing agent. Here's the URL, scenario, and screenshot."
        2. Assistant: Returns function call (goto, click, fill, etc.) 
        3. System: Execute function, take screenshot, feed back to LLM
        4. Loop until agent calls "finish"
        
        Args:
            url: The website URL to test
            scenario: Description of the user scenario to test
            
        Returns:
            Dictionary with analysis results and action history
        """
        print(f"🎯 Starting interactive scenario analysis")
        print(f"🌐 Target URL: {url}")
        print(f"📝 Scenario: {scenario}")
        
        # Get batch optimization suggestions
        batch_suggestions = self._suggest_batch_optimizations(scenario)
        if batch_suggestions:
            print("🔄 Batching Suggestions:")
            print(batch_suggestions)
            print()
        
        try:
            with LocalPlaywrightBrowser() as browser:
                page = browser.page
                self.browser_tools = BrowserTools(page)
                
                # Initialize the conversation with system and user prompts
                messages = [
                    {
                        "role": "system",
                        "content": self._build_interactive_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": self._build_scenario_prompt(url, scenario)
                    }
                ]
                
                actions_taken = []
                action_count = 0
                
                print(f"\\n🚀 Starting interactive loop...")
                
                # Interactive Loop: Keep calling GPT-4o until it calls "finish"
                while action_count < self.max_actions:
                    print(f"\\n🔄 Turn {action_count + 1}/{self.max_actions}")
                    
                    # Call GPT-4o with function calling using rate-limited client
                    try:
                        # Convert BROWSER_FUNCTIONS to tools format
                        tools = [{"type": "function", "function": func} for func in BROWSER_FUNCTIONS]
                        
                        response = self.client.chat_completion(
                            messages=messages,
                            tools=tools,
                            tool_choice="auto",
                            temperature=0.1,
                            max_tokens=2000,
                            enable_fallback=self.enable_fallback
                        )
                        
                        message = response.choices[0].message
                        
                        # Add assistant message to conversation
                        messages.append({
                            "role": "assistant",
                            "content": message.content,
                            "tool_calls": message.tool_calls if message.tool_calls else None
                        })
                        
                        # Check if assistant wants to call a function
                        if message.tool_calls:
                            # Process all tool calls in this turn (batching support)
                            turn_actions = []
                            should_break = False
                            
                            for tool_call in message.tool_calls:
                                func_name = tool_call.function.name
                                func_args = json.loads(tool_call.function.arguments)
                                
                                print(f"🔧 Agent calling: {func_name}({func_args})")
                                
                                # Execute the function against browser tools
                                if hasattr(self.browser_tools, func_name):
                                    func = getattr(self.browser_tools, func_name)
                                    action_result = func(**func_args)
                                    actions_taken.append(action_result)
                                    turn_actions.append(action_result)
                                    
                                    print(f"✅ Action result: {action_result.get('message', 'No message')}")
                                    
                                    # Add function result to conversation 
                                    function_response = {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "content": json.dumps(action_result, indent=2)
                                    }
                                    messages.append(function_response)
                                    
                                    # Check if agent called "finish" 
                                    if func_name == "finish":
                                        print("🏁 Agent called finish - scenario complete!")
                                        should_break = True
                                        break
                                        
                                else:
                                    error_msg = f"Unknown function: {func_name}"
                                    print(f"❌ {error_msg}")
                                    messages.append({
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "content": json.dumps({"error": error_msg})
                                    })
                            
                            # Take a single screenshot after all actions in this turn (optimization)
                            if turn_actions and not should_break:
                                # Only take screenshot if no screenshot was already taken in this turn
                                screenshot_taken_this_turn = any(
                                    action.get('action') == 'screenshot' for action in turn_actions
                                )
                                
                                if not screenshot_taken_this_turn:
                                    screenshot_result = self.browser_tools.screenshot()
                                    if screenshot_result.get("success") and screenshot_result.get("screenshot_base64"):
                                        # Add screenshot to next turn
                                        screenshot_msg = {
                                            "role": "user",
                                            "content": [
                                                {
                                                    "type": "text", 
                                                    "text": f"Here's the current state after {len(turn_actions)} actions:"
                                                },
                                                {
                                                    "type": "image_url",
                                                    "image_url": {
                                                        "url": f"data:image/png;base64,{screenshot_result['screenshot_base64']}"
                                                    }
                                                }
                                            ]
                                        }
                                        messages.append(screenshot_msg)
                            
                            if should_break:
                                break
                        
                        elif message.content:
                            # Agent is speaking but not calling functions - might be analysis
                            print(f"💬 Agent message: {message.content}")
                            
                            # If agent seems done without calling finish, break
                            done_keywords = ['analysis complete', 'task complete', 'done', 'finished', 'unable to proceed']
                            if any(keyword in message.content.lower() for keyword in done_keywords):
                                print("✅ Agent indicates completion via message")
                                break
                        
                        action_count += 1
                        
                    except Exception as e:
                        print(f"❌ Error in interactive loop: {e}")
                        break
                
                # Perform final UX analysis on the last screenshot
                print(f"\\n🔍 Performing final UX analysis...")
                final_analysis = self._perform_final_ux_analysis()
                
                # Get client usage statistics
                client_stats = self.client.get_stats()
                
                return {
                    "status": "success",
                    "scenario": scenario,
                    "url": url, 
                    "actions_taken": actions_taken,
                    "action_count": action_count,
                    "conversation_turns": len(messages),
                    "final_analysis": final_analysis,
                    "client_stats": client_stats,
                    "raw_conversation": messages  # For debugging
                }
                
        except Exception as e:
            print(f"❌ Error in scenario analysis: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "scenario": scenario,
                "url": url,
                "client_stats": self.client.get_stats()
            }
    
    def get_client_stats(self) -> Dict[str, Any]:
        """Get OpenAI client usage statistics."""
        return self.client.get_stats()
    
    def reset_client_stats(self):
        """Reset OpenAI client usage statistics."""
        self.client.reset_stats()
    
    def _build_interactive_system_prompt(self) -> str:
        """Build the system prompt for the interactive testing loop."""
        return """You are a UX testing agent that performs interactive browser testing scenarios.

🎯 YOUR ROLE:
- You will be given a website URL and a specific user scenario to test
- Your job is to navigate and interact with the website like a real user would
- Use the available browser functions to perform actions step by step
- Take screenshots and analyze what you see to guide your next actions
- Complete the scenario and report on any UX issues you discover

🔧 AVAILABLE BROWSER FUNCTIONS:
- goto(url): Navigate to a URL
- click(selector, description): Click an element using CSS selector  
- fill(selector, text, description): Fill in form fields
- wait_for_element(selector, timeout): Wait for an element to appear
- scroll_to(selector): Scroll to an element
- screenshot(): Take a screenshot of current page
- get_page_info(): Get page title, URL, and basic info
- find_elements(description): Find elements by description
- finish(analysis, task_completed): Signal completion and provide final analysis

🎬 TESTING PROTOCOL:
1. Start by navigating to the given URL using goto()
2. Take a screenshot to see the current state  
3. Analyze what you see and plan your next action
4. Perform actions step by step toward completing the scenario
5. Take screenshots after major actions to see results
6. If you encounter issues, try alternative approaches
7. When done, call finish() with your analysis

💡 BEST PRACTICES:
- Always start with goto() to navigate to the target URL
- Use descriptive text when clicking/filling (helps with debugging)
- Take screenshots periodically to see current state
- Look for UX issues: accessibility, usability, design problems
- Be thorough but efficient - aim for 5-10 actions total
- If an element is hard to find, use find_elements() first
- Always call finish() when the scenario is complete or impossible

⚡ EFFICIENCY TIPS:
- You can call multiple functions in sequence if they're related
- When you need to analyze the page state, take a screenshot immediately
- If you plan to find and then click an element, you can do both in the same turn
- Batch related operations to minimize round-trips

🚨 IMPORTANT:
- Only call functions, don't provide explanatory text unless asked
- Each response should contain one or more function calls
- Screenshots will be provided to you after each action
- Focus on completing the specific scenario given
- Report both successful task completion AND any UX issues discovered"""

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent."""
        return """You are a UX testing expert with the ability to interact with web pages.

Your goal is to test user scenarios by:
1. Navigating to pages
2. Interacting with elements (clicking, filling forms, etc.)
3. Observing the results
4. Identifying UX issues and improvements

Available tools:
- goto: Navigate to a URL
- click: Click on elements
- fill: Fill form inputs
- wait_for_element: Wait for elements to appear
- screenshot: Take screenshots for analysis
- get_page_info: Get current page details
- find_elements: Find elements by description
- scroll_to: Scroll to elements

Guidelines:
- Always take a screenshot first to see the current state
- Be methodical - complete one action before planning the next
- Describe what you're looking for before trying to interact
- If an element isn't found, try find_elements to explore alternatives
- Take screenshots after significant actions to verify results
- Provide clear reasoning for each action
- Identify UX issues as you encounter them
- When the scenario is complete or impossible, say "ANALYSIS COMPLETE"

Remember: You're testing from a real user's perspective. Note any friction, confusion, or obstacles."""
    
    def _build_scenario_prompt(self, url: str, scenario: str) -> str:
        """Build the initial scenario prompt."""
        return f"""Please test this user scenario:

SCENARIO: {scenario}
TARGET URL: {url}

Start by navigating to the URL and taking a screenshot to see the current state. Then work through the scenario step by step, taking actions as needed and noting any UX issues you encounter.

Focus on:
- How easy/difficult it is to complete the scenario
- Any confusing or unclear interface elements
- Missing functionality or broken features
- Accessibility concerns
- Overall user experience quality

Begin by going to the URL."""
    
    def _call_gpt4o(self) -> Optional[Any]:
        """Call GPT-4o with current conversation history."""
        try:
            response = self.client.chat_completion(
                model=self.model,
                messages=self.conversation_history,
                tools=[{"type": "function", "function": func} for func in BROWSER_FUNCTIONS],
                max_tokens=1000
            )
            return response
            
        except Exception as e:
            print(f"❌ Error calling GPT-4o: {e}")
            return None
    
    def _execute_function_call(self, tool_call) -> Dict[str, Any]:
        """Execute a function call from GPT-4o."""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 Executing: {function_name}({arguments})")
        
        # Map function names to BrowserTools methods
        if hasattr(self.browser_tools, function_name):
            method = getattr(self.browser_tools, function_name)
            result = method(**arguments)
            
            print(f"✅ Result: {result.get('message', 'No message')}")
            return result
        else:
            error_result = {
                "success": False,
                "action": function_name,
                "error": f"Unknown function: {function_name}",
                "message": f"Function {function_name} not available"
            }
            print(f"❌ {error_result['message']}")
            return error_result
    
    def _perform_final_ux_analysis(self) -> Dict[str, Any]:
        """Perform final UX analysis based on the testing session."""
        try:
            # Take a final screenshot
            final_screenshot = self.browser_tools.screenshot()
            
            # Build analysis prompt
            analysis_prompt = """Based on the interactive testing session we just completed, please provide a comprehensive UX analysis.

Focus on:
1. Issues encountered during the scenario execution
2. Usability problems that would affect real users
3. Areas for improvement
4. Positive aspects of the user experience

Return your analysis as a JSON array of findings, where each finding has:
- category: type of issue (e.g., "Navigation", "Forms", "Content", "Accessibility", "Performance")
- item: brief description
- description: detailed explanation of the issue and impact
- severity: "high", "medium", or "low"
- scenario_impact: how this affects the specific scenario tested

Respond only with valid JSON."""
            
            # Add analysis request to conversation
            analysis_messages = self.conversation_history + [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": analysis_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{final_screenshot['screenshot_data']}"
                            }
                        }
                    ]
                }
            ]
            
            # Get analysis from GPT-4o
            response = self.client.chat_completion(
                model=self.model,
                messages=analysis_messages,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                if "```json" in analysis_text:
                    start = analysis_text.find("```json") + 7
                    end = analysis_text.find("```", start)
                    analysis_text = analysis_text[start:end].strip()
                elif "```" in analysis_text:
                    start = analysis_text.find("```") + 3
                    end = analysis_text.find("```", start)
                    analysis_text = analysis_text[start:end].strip()
                
                issues = json.loads(analysis_text)
                
                return {
                    "success": True,
                    "issues": issues,
                    "raw_analysis": analysis_text
                }
                
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                return {
                    "success": True,
                    "issues": [{
                        "category": "Analysis",
                        "item": "UX Assessment",
                        "description": analysis_text,
                        "severity": "medium",
                        "scenario_impact": "Overall assessment of scenario completion"
                    }],
                    "raw_analysis": analysis_text
                }
                
        except Exception as e:
            print(f"❌ Error in final analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "issues": []
            }
