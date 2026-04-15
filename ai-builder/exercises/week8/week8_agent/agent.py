# agent.py
# Main agent loop for the Week 8 tool-using agent.
#
# The agent accepts a plain text task, then repeatedly:
#   1. Calls Claude with the current message history and available tools.
#   2. Checks stop_reason — if "end_turn" it prints the final answer.
#   3. If the model wants tools, executes them and feeds results back.
#
# Run normally:  python agent.py          (runs the default demo task)
# Run all tests: set RUN_TESTS = True then python agent.py

import os
import json
from dotenv import load_dotenv
import anthropic

from tool_schemas import TOOL_SCHEMAS
from tools import search_notes, calculate, summarize_text, save_result, think

# ── Configuration ────────────────────────────────────────────────────────────

# Set to True to run all 5 evaluation tasks and save test_results.json.
# Leave False to run just the single demo task.
RUN_TESTS = True

MODEL = "claude-haiku-4-5-20251001"
MAX_ITERATIONS = 10

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to notes, a calculator, "
    "summarization, and file saving. Use tools when needed to complete tasks."
)

# Map tool names (as the model knows them) to actual Python functions.
# The model calls tools by name — this dict is how we dispatch the call.
TOOL_FUNCTIONS = {
    "search_notes": search_notes,
    "calculate": calculate,
    "summarize_text": summarize_text,
    "save_result": save_result,
    "think": think,
}

# Anchor the results/ folder to this file's location, not the CWD.
_BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(_BASE_DIR, "results")

# ── Core agent function ───────────────────────────────────────────────────────

def run_agent(user_input, client):
    """
    Run the agent loop for a single task.

    The loop calls Claude, checks whether it wants tools or is done,
    executes tools if requested, and feeds results back until end_turn.

    Args:
        user_input (str): The task or question for the agent.
        client (anthropic.Anthropic): A shared Anthropic client.

    Returns:
        dict: {
            "answer": str,        — the final text response from Claude
            "steps": int,         — how many loop iterations were used
            "tools_used": list    — names of every tool that was called
        }
    """
    # Start with just the user's task in the message history.
    # Each loop iteration will append the assistant response and tool results.
    messages = [{"role": "user", "content": user_input}]

    iteration = 0
    tools_used = []  # track which tools the agent called

    while iteration < MAX_ITERATIONS:
        iteration += 1

        # ── Call Claude ──────────────────────────────────────────────────────
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        # Append the full assistant response to history so Claude remembers it.
        messages.append({"role": "assistant", "content": response.content})

        # ── Check stop reason ────────────────────────────────────────────────
        if response.stop_reason == "end_turn":
            # The model is finished — extract the final text and return.
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                ""
            )
            return {
                "answer": final_text,
                "steps": iteration,
                "tools_used": tools_used
            }

        # ── Execute tools ────────────────────────────────────────────────────
        # The model returned one or more tool_use blocks.
        # Run each tool, collect results, send them back as a user message.
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                if block.name == "think":
                    print(f"  Step {iteration}: [thinking] {block.input.get('thought', '')[:100]}")
                else:
                    print(f"  Step {iteration}: calling {block.name}")
                tools_used.append(block.name)

                # Dispatch to the matching Python function
                tool_fn = TOOL_FUNCTIONS[block.name]
                try:
                    result = tool_fn(**block.input)
                except Exception as e:
                    result = f"Error in {block.name}: {type(e).__name__}: {e}"

                # Tool results must be strings; convert anything that isn't
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,   # must match the tool_use block's id
                    "content": str(result)
                })

        # Feed all tool results back to Claude as a user message
        messages.append({"role": "user", "content": tool_results})

    # Reached max iterations without an end_turn — return a safe fallback
    return {
        "answer": "Max iterations reached without a final answer.",
        "steps": iteration,
        "tools_used": tools_used
    }


# ── Evaluation tasks ──────────────────────────────────────────────────────────

# Five test tasks that exercise all four tools in various combinations.
TEST_TASKS = [
    "What is 847 times 23?",
    "Find my notes about functions",
    "Find my notes about APIs and summarize them",
    "What is 15% of 2340, and save the result as tip_calc.txt",
    "Find my notes about agents, summarize them, and save as agent_summary.txt",
]


def run_evaluation(client):
    """
    Run all TEST_TASKS through the agent and save a summary to test_results.json.

    Each result captures:
      - task       : the original task string
      - completed  : True if we got a non-empty, non-timeout answer
      - steps      : number of agent loop iterations used
      - tools_used : list of tool names called (may contain duplicates)

    Args:
        client (anthropic.Anthropic): A shared Anthropic client.
    """
    results = []

    print(f"\n{'='*60}")
    print("Running evaluation — 5 tasks")
    print('='*60)

    for i, task in enumerate(TEST_TASKS, start=1):
        print(f"\nTask {i}/{len(TEST_TASKS)}: {task}")
        print("-" * 50)

        result = run_agent(task, client)

        # A task is "completed" if we got a real answer before hitting max iterations.
        completed = bool(
            result["answer"]
            and result["answer"] != "Max iterations reached without a final answer."
        )

        task_record = {
            "task": task,
            "completed": completed,
            "steps": result["steps"],
            "tools_used": result["tools_used"]
        }
        results.append(task_record)

        status = "PASS" if completed else "FAIL"
        print(f"  [{status}] {result['steps']} steps, tools: {result['tools_used']}")
        print(f"  Answer: {result['answer'][:200]}{'...' if len(result['answer']) > 200 else ''}")

    # Save the summary to results/test_results.json
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, "test_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    passed = sum(1 for r in results if r["completed"])
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{len(results)} tasks completed")
    print(f"Saved: results/test_results.json")
    print('='*60)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Load ANTHROPIC_API_KEY from the .env file before creating the client.
    load_dotenv()
    client = anthropic.Anthropic()

    if RUN_TESTS:
        run_evaluation(client)
    else:
        # Default demo task — change this string to try different things.
        task = "Find my notes about APIs and summarize them"

        print(f"Task: {task}")
        print("-" * 50)

        result = run_agent(task, client)

        print(f"\nAnswer:\n{result['answer']}")
        print(f"\n[{result['steps']} step(s), tools used: {result['tools_used']}]")
