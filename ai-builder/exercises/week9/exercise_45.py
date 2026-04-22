class TaskState:
    def __init__(self, task: str):
        self.task = task
        self.status = "running"
        self.steps_taken = []
        self.results = {}
        self.tool_call_count = 0
        self.errors = []

    def add_step(self, description: str):
        self.steps_taken.append(description)
        print(f"[Step {len(self.steps_taken)}] {description}")

    def add_result(self, key:str, value: str):
        self.results[key] = value
        print(f"[Result saved] {key}")

    def add_error(self, error: str):
        self.errors.append(error)
        print(f"[Error] {error}")

    def complete(self):
        self.status = "complete"
        print(f"=== Task Complete ===")
        print(f"Task: {self.task}")
        print(f"Steps Taken: {len(self.steps_taken)}")
        print(f"Results: {", ".join(self.results.keys())}")
        print(f"Errors: {len(self.errors)}")
    
    def summary_for_claude(self) -> str:
        recent = " | ".join(self.steps_taken[-3:])
        result_keys = ", ".join(self.results.keys())
        return (
            f"Task: {self.task}\n"
            f"Steps taken: {len(self.steps_taken)}\n"
            f"Recent steps: {recent}\n"
            f"Results accumulated: {result_keys}\n"
            f"Errors so far: {len(self.errors)}"
        )
    

if __name__ == "__main__":
    state = TaskState("Analyze Q3 sales data and save a summary")
    state.add_step("Searched sales database")
    state.add_step("Filtered to Q3 entries")
    state.add_step("Calculated totals")
    state.add_result("total_revenue", "$1.2M")
    state.add_result("top_product", "Solar Panel A")
    state.add_error("Missing data for September week 3")
    state.add_step("Generated summary despite missing data")
    
    print("\n--- Summary for Claude ---")
    print(state.summary_for_claude())
    
    state.complete()