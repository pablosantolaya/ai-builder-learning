# agent.py
# Week 9 agent — adds TaskState tracking and HITL approval to the week8 loop.
#
# New behaviour vs week8:
#   - Every tool call is logged to a TaskState object (steps, results, errors)
#   - Dangerous tools (save_result) require human approval before running
#   - run_agent() returns the TaskState instead of a plain dict
#
# Run normally:  python agent.py          (runs the default demo task)
# Run all tests: set RUN_TESTS = True then python agent.py

import os
import json
from dotenv import load_dotenv
import anthropic

from tool_schemas import TOOL_SCHEMAS
from tools import search_notes, calculate, summarize_text, save_result, think
from state import TaskState                        # NEW: task logbook
from hitl import run_tool_with_approval, classify            # NEW: approval gate

# ── Configuration ─────────────────────────────────────────────────────────────

RUN_TESTS = True   # Set True to run all 5 evaluation tasks

MODEL = "claude-haiku-4-5-20251001"
MAX_ITERATIONS = 10

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to notes, a calculator, "
    "summarization, and file saving. Use tools when needed to complete tasks."
)

# Maps tool names → Python functions.
# run_tool_with_approval receives this dict and calls the right function.
TOOL_FUNCTIONS = {
    "search_notes": search_notes,
    "calculate": calculate,
    "summarize_text": summarize_text,
    "save_result": save_result,
    "think": think,
}

_BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(_BASE_DIR, "results")

# ── Core agent function ────────────────────────────────────────────────────────

def run_agent(user_input, client):
    """
    Run the agent loop for a single task.

    Calls Claude repeatedly until it signals end_turn or we hit MAX_ITERATIONS.
    Every tool call is routed through the HITL gate and logged to TaskState.

    Args:
        user_input (str): The task or question for the agent.
        client (anthropic.Anthropic): A shared Anthropic client.

    Returns:
        TaskState: The completed state object. Read .answer for the final text,
                   .steps_taken for the log, .errors for anything that went wrong.
    """
    messages = [{"role": "user", "content": user_input}]

    # NEW: create the logbook for this run
    state = TaskState(task=user_input)

    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1

        # ── Call Claude ───────────────────────────────────────────────────────
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        messages.append({"role": "assistant", "content": response.content})

        # ── Check stop reason ─────────────────────────────────────────────────
        if response.stop_reason == "end_turn":
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                ""
            )
            state.answer = final_text   # NEW: store final answer on state
            state.complete()            # NEW: mark done, print summary
            return state                # NEW: return state instead of dict

        # ── Execute tools ─────────────────────────────────────────────────────
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                # Log the step before calling anything
                state.add_step(f"Calling {block.name} with {block.input}")
                state.tools_used.append(block.name)

                # All calls go through the HITL gate; returns a ToolResult
                tool_result = run_tool_with_approval(block.name, block.input, TOOL_FUNCTIONS)

                # Classify the result into a recovery strategy
                recovery = classify(tool_result)

                # Decide what to log and what to send back to Claude
                if recovery == "ok":
                    state.add_result(block.name, tool_result.data)
                    content_for_claude = tool_result.data

                elif recovery == "retry":
                    if state.can_retry(block.name):
                        state.record_retry(block.name)
                        state.add_error(
                            f"{block.name}: transient error (will retry): {tool_result.message}"
                        )
                        content_for_claude = (
                            f"Transient error: {tool_result.message}. "
                            f"You may retry this tool call."
                        )
                    else:
                        state.add_error(
                            f"{block.name}: retry limit reached: {tool_result.message}"
                        )
                        content_for_claude = (
                            f"Retry limit reached for {block.name}: {tool_result.message}. "
                            f"Do not retry this tool; try a different approach or stop."
                        )

                elif recovery == "modify_input":
                    state.add_error(
                        f"{block.name}: input error: {tool_result.message}"
                    )
                    content_for_claude = (
                        f"Input error: {tool_result.message}. "
                        f"Reformulate the arguments and try again, or try a different tool."
                    )

                else:  # "give_up"
                    state.add_error(
                        f"{block.name}: fundamental error: {tool_result.message}"
                    )
                    content_for_claude = (
                        f"Fundamental error: {tool_result.message}. "
                        f"Do not retry. Try a different approach or stop."
                    )

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content_for_claude
                })

        messages.append({"role": "user", "content": tool_results})

    # Hit max iterations — return state as-is (status stays "running")
    state.answer = "Max iterations reached without a final answer."
    return state


# ── Evaluation tasks ───────────────────────────────────────────────────────────

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
    """
    results = []

    print(f"\n{'='*60}")
    print("Running evaluation — 5 tasks")
    print('='*60)

    for i, task in enumerate(TEST_TASKS, start=1):
        print(f"\nTask {i}/{len(TEST_TASKS)}: {task}")
        print("-" * 50)

        state = run_agent(task, client)   # now returns TaskState

        completed = bool(
            state.answer
            and state.answer != "Max iterations reached without a final answer."
        )

        task_record = {
            "task": state.task,
            "completed": completed,
            "steps": len(state.steps_taken),
            "tools_used": state.tools_used
        }
        results.append(task_record)

        status = "PASS" if completed else "FAIL"
        print(f"  [{status}] {len(state.steps_taken)} steps, tools: {state.tools_used}")
        print(f"  Answer: {state.answer[:200]}{'...' if len(state.answer) > 200 else ''}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, "test_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    passed = sum(1 for r in results if r["completed"])
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{len(results)} tasks completed")
    print(f"Saved: results/test_results.json")
    print('='*60)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    load_dotenv()
    client = anthropic.Anthropic()

    if RUN_TESTS:
        run_evaluation(client)
    else:
        task = "Find my notes about APIs and summarize them"

        print(f"Task: {task}")
        print("-" * 50)

        state = run_agent(task, client)

        print(f"\n--- Final Answer ---")
        print(state.answer)
        print(f"\n--- State Summary ---")
        print(state.summary_for_claude())
