# state.py
# Tracks everything that happens during a single agent run.
# Think of TaskState as a logbook: the agent writes to it as it works,
# and we can read it at any point to see what happened.

class TaskState:
    def __init__(self, task: str):
        self.task = task              # The original user request
        self.status = "running"       # "running" → "complete" when done
        self.steps_taken = []         # List of description strings, one per tool call
        self.results = {}             # Dict: tool_name → result string
        self.errors = []              # List of error strings
        self.answer = ""              # The final text Claude returns at end_turn
        self.tools_used = []          # List of tool names called (for run_evaluation)
        self.retry_counts = {}        # Dict: tool_name → number of retries

    def add_step(self, description: str):
        """Log that a tool call is about to happen."""
        self.steps_taken.append(description)
        print(f"[Step {len(self.steps_taken)}] {description}")

    def add_result(self, key: str, value: str):
        """Store a successful tool result."""
        self.results[key] = value
        print(f"[Result saved] {key}")

    def add_error(self, error: str):
        """Store an error (tool failure or user cancel)."""
        self.errors.append(error)
        print(f"[Error] {error}")

    def complete(self):
        """Mark the task done and print a summary."""
        self.status = "complete"
        print(f"\n=== Task Complete ===")
        print(f"Task: {self.task}")
        print(f"Steps taken: {len(self.steps_taken)}")
        print(f"Results: {', '.join(self.results.keys()) or 'none'}")
        print(f"Errors: {len(self.errors)}")

    def summary_for_claude(self) -> str:
        """
        A compact status string we can print after the run.
        Shows the last 3 steps so you can see what the agent did recently.
        """
        recent = " | ".join(self.steps_taken[-3:]) if self.steps_taken else "none"
        result_keys = ", ".join(self.results.keys()) or "none"
        return (
            f"Task: {self.task}\n"
            f"Steps taken: {len(self.steps_taken)}\n"
            f"Recent steps: {recent}\n"
            f"Results accumulated: {result_keys}\n"
            f"Errors so far: {len(self.errors)}"
        )

    def record_retry(self, tool_name: str):
        """Increment the retry count for a given tool."""
        if tool_name not in self.retry_counts:
            self.retry_counts[tool_name] = 0
        self.retry_counts[tool_name] += 1
        print(f"[Retry] {tool_name} has been retried {self.retry_counts[tool_name]} times")

    def can_retry(self, tool_name: str, max_retries: int = 3) -> bool:
        """Check if we can retry a tool based on how many times we've retried it already."""
        retries = self.retry_counts.get(tool_name, 0)
        return retries < max_retries
