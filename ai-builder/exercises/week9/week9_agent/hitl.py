# hitl.py
# Human-in-the-loop (HITL) approval gate for dangerous tool calls.
# Before a dangerous tool runs, the user is asked to approve or cancel it.
# Imported by agent.py — every tool call passes through run_tool_with_approval().

# Tools that require human approval before they run.
# "save_result" writes to disk, so we treat it as dangerous.
DANGEROUS_TOOLS = {"save_result"}

from dataclasses import dataclass, field

@dataclass
class ToolResult:
    status: str
    data: str | None = None
    error_type: str | None = None
    message: str | None = None


def requires_approval(tool_name: str) -> bool:
    """Return True if this tool needs human sign-off before running."""
    return tool_name in DANGEROUS_TOOLS


def request_approval(tool_name: str, tool_args: dict) -> bool:
    """
    Print the tool name and its arguments, then block on user input.
    Returns True if the user typed 'y', False for anything else.
    """
    print(f"\nAPPROVAL REQUIRED")
    print(f"Tool:  {tool_name}")
    print(f"Input: {tool_args}")
    response = input("Approve? (y/n): ")
    return response.strip().lower() == "y"


def classify(result):
    if result.status == "success":
        return "ok"
    elif result.error_type == "transient":
        return "retry"
    elif result.error_type == "input":
        return "modify_input"
    elif result.error_type == "fundamental":
        return "give_up"
    else:
        return "give_up"
    
def classify_exception(e: Exception) -> str:
    """Map a caught exception to an error_type for ToolResult."""
    if isinstance(e, (TimeoutError, ConnectionError)):
        return "transient"
    if isinstance(e, (ValueError, KeyError, TypeError)):
        return "input"
    if isinstance(e, (FileNotFoundError, PermissionError)):
        return "fundamental"
    return "fundamental"  # unknown → safest default

def run_tool_with_approval(tool_name: str, tool_args: dict, dispatch: dict) -> ToolResult:
    """
    Guard-first dispatch — checks safety before calling anything.

    Order of checks:
      1. Unknown tool  → return an error string immediately
      2. Safe tool     → call it directly, return result
      3. Dangerous     → ask for approval:
                           approved  → call it, return result
                           rejected  → return cancellation string

    Args:
        tool_name (str): Name of the tool the model wants to call.
        tool_args (dict): The arguments block.input from the API response.
        dispatch (dict): Maps tool names → Python functions (TOOL_FUNCTIONS).

    Returns:
        str: The tool result, an error string, or the cancellation string.
    """
    # Guard 1: unknown tool — stop immediately, don't try to call anything
    if tool_name not in dispatch:
        return ToolResult(
            status="error",
            error_type="fundamental",
            message=f"Unknown tool '{tool_name}'"
        )
    
    # Guard 2: safe tool — call directly using **kwargs to unpack the args dict
    if not requires_approval(tool_name):
        try:
            result = dispatch[tool_name](**tool_args)
            return ToolResult(status="success", data=str(result))
        except Exception as e:
            return ToolResult(
                status="error",
                error_type=classify_exception(e),
                message=f"{type(e).__name__}: {e}"
            )

    # Guard 3: dangerous tool — ask the user first
    approved = request_approval(tool_name, tool_args)
    if not approved:
        return ToolResult(
            status="error",
            error_type="fundamental",
            message="User cancelled the operation"
        )

    try:
        result = dispatch[tool_name](**tool_args)
        return ToolResult(status="success", data=str(result))
    except Exception as e:
        return ToolResult(
            status="error",
            error_type=classify_exception(e),
            message=f"{type(e).__name__}: {e}"
        )

