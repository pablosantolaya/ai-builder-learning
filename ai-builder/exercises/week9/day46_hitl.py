DANGEROUS_TOOLS = {"send_email", "delete_file", "post_to_slack"}

def requires_approval(tool_name: str):
    return tool_name in DANGEROUS_TOOLS
    
def request_approval(tool_name: str, tool_input: dict):
    print(f"APPROVAL REQUIRED")
    print(f"<{tool_name}>")
    print(f"Input: <{tool_input}>")
    response = input("Approve? (y/n): ")
    
    if response.strip().lower() == "y":
        return True
    else:
        return False
    
def run_tool_with_approval(tool_name: str, tool_input: dict, dispatch: dict):
    if tool_name not in dispatch:
        return f"Unknown tool: {tool_name}"
    
    if requires_approval(tool_name):
        response = request_approval(tool_name, tool_input)
        if response:
            result = dispatch[tool_name](tool_input)
            return result
        else:
            return f"Action cancelled by user: <{tool_name}>"
    else:
        result = dispatch[tool_name](tool_input)
        return result
    
    
if __name__ == "__main__":
    # Mock tools
    def send_email(to: str, subject: str, body: str) -> str:
        return f"Email sent to {to}: '{subject}'"
    
    def search_notes(query: str) -> str:
        return f"Found 3 notes matching '{query}'"
    
    dispatch = {
        "send_email": lambda args: send_email(**args),
        "search_notes": lambda args: search_notes(**args)
    }
    
    # Test 1: safe tool (no approval needed)
    print("--- Test 1: Safe tool ---")
    result = run_tool_with_approval(
        "search_notes",
        {"query": "Q3 revenue"},
        dispatch
    )
    print(f"Result: {result}\n")
    
    # Test 2: dangerous tool (approval required)
    print("--- Test 2: Dangerous tool ---")
    result = run_tool_with_approval(
        "send_email",
        {"to": "cfo@company.com", "subject": "Q3 Report", "body": "See attached."},
        dispatch
    )
    print(f"Result: {result}")