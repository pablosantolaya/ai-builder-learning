# AI Builder Roadmap v3 — Updated Plan

## Pablo's Profile

- MIT MBA student, 5 years startup experience (property, energy, back-office ops)
- Strong prompt engineering (built negotiation agents, customer support agents, system prompts with phased strategies)
- Python skill level: ~5/10 after completing Phase 1 (can write multi-file projects, call APIs, handle errors, parse structured outputs)
- Tools installed and configured: VS Code (with Python extension), Git + GitHub CLI, Claude Code, Python, Node.js
- Weekly time: 5-8 hours in dedicated blocks, occasional longer weekend sessions
- Priority stack: Deep AI knowledge (agents, MCP, orchestration) → Python fluency → AI consulting for enterprises → AI-native B2B startup
- Industries: Energy operations, back-office automation, enterprise (McKinsey-tier use cases)
- Learning style: Conceptual understanding first, then structured exercises, then build projects. Reviews proposed changes before approving.
- Semester deadline: May 29, 2026 (but learning continues after graduation — no hard cutoff)

---

## How This Roadmap Is Organized

### The Four Learning Tiers

Everything you could learn falls into four tiers. The roadmap prioritizes Tiers 1–3, with Tier 4 as post-roadmap exploration.

**Tier 1 — Core Skills (Must Learn):** Python gaps, tool calling, agent architecture, prompt chaining
**Tier 2 — Ecosystem & Tools (Should Learn):** MCP, Claude Code skills/subagents, Cowork, Claude Code Agent Teams
**Tier 3 — AI Stack Knowledge (Should Understand):** RAG, embeddings, fine-tuning/LoRA, the consulting decision framework
**Tier 4 — Advanced (Post-Roadmap):** Multi-agent orchestration frameworks, async Python, LangChain/CrewAI, open-source model hosting, Docker

### Session Structure

Each session follows this pattern:

```
1. WARM-UP (5 min)
   - Quick exercise reinforcing a concept from a previous week
   - Goal: move skills from "Familiar" to "Comfortable"

2. LEARN (30-45 min)
   - New concept taught in Claude Chat
   - Structured exercises written by hand in VS Code

3. BUILD (45-60 min)
   - Apply the concept in a project
   - Claude Code for builds, hand-coding for exercises

4. WRAP-UP (10 min)
   - Update Progress Log, Skills Tracker, Cheat Sheet
   - Session Handoff Block for next time
```

### How Each Week Works

```
DAY 1 (1.5-2h): PYTHON + CONCEPT
  - Warm-up exercise from a previous topic
  - Learn new Python concepts + new AI concept
  - Structured exercises in VS Code

DAY 2 (1.5-2h): BUILD
  - Plan the project in Claude Chat
  - Build with Claude Code (or by hand for reinforcement)
  - Test and debug

DAY 3 (1.5-2h): EXTEND + COMMIT
  - Add a feature yourself (without Claude Code)
  - Debug with Claude Code as helper
  - Commit to Git, update Progress Log
  - Update Skills Tracker and Cheat Sheet
```

---

## Completed Phases (For Reference)

### Phase 0: Setup & Orientation (Days 1-3) ✅

- Environment setup: VS Code, Python extension, Git, GitHub CLI, Claude Code, Node.js
- Claude Code orientation: first session, safety setup (settings.json + CLAUDE.md)
- Git foundations: branching, merging, pushing to GitHub
- Claude Project configured with roadmap, progress log, skills tracker

### Phase 1: Python Foundations + First Tools (Weeks 1-3) ✅

- **Week 1:** Variables, types, strings, f-strings, lists, dictionaries, functions, loops, conditionals, file I/O, JSON. Built Text File Analyzer.
- **Week 2:** Error handling, imports, pip, environment variables, APIs/HTTP, Anthropic SDK. Built Document Summarizer (with Claude Code), extended independently.
- **Week 3:** Classes, argparse, multi-file project structure, structured outputs from LLMs. Built Meeting Notes Processor (entirely by hand), extended with follow-up email + Git branching.

**Python skills after Phase 1:** 35+ concepts at "Familiar" level, 25+ at "Introduced" level. Can write multi-file Python projects that call Claude's API, handle errors, parse structured outputs, and save results.

---

## Phase 2: Real Tools + Prompt Chaining (Weeks 4-7)

**Goal:** Fill remaining Python gaps, build tools you could actually use, learn prompt chaining and multi-turn API conversations. Introduce MCP conceptually and Claude Code skills creation. By the end of this phase, you can build multi-step AI tools that process real data, and you understand how MCP connects AI to external services.

### Week 4: Dates, Sorting, and the Email/Calendar Briefing

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write a function from memory that takes a list of dictionaries and returns them filtered by a field value (reinforces Day 2 patterns).

New Python concepts: List comprehensions, datetime module, sorting with key functions

```
Exercise 29: List comprehensions — rewrite these for-loop patterns as one-liners:
  a) Filter a list of numbers to only even ones
  b) Create a list of uppercase versions of a list of strings
  c) Extract just the "name" field from a list of student dictionaries
  Compare readability: when is a list comprehension clearer vs. a for loop?

Exercise 30: Dates and times —
  a) Get today's date and print it in "March 23, 2026" format
  b) Calculate how many days until May 29, 2026 (your deadline)
  c) Given a time string like "14:30", determine if it's morning, afternoon, or evening
  d) Create a list of the next 7 days with their day-of-week names

Exercise 31: Sorting —
  a) Given a list of dicts representing emails (with "from", "subject", "date", "body"), 
     sort them by date (newest first)
  b) Add a "priority" field based on keywords in the subject ("urgent", "deadline", "ASAP" = high)
  c) Return only the high-priority emails, sorted by date
```

New AI concept: **Prompt chaining** — breaking a complex task into sequential LLM calls where each output feeds the next. Why: single prompts have limits; chaining lets you decompose problems.

```
Exercise 32: Prompt chaining exercise —
  a) Write a function chain_summarize_then_extract(text) that:
     - Call 1: Sends text to Claude asking for a summary
     - Call 2: Sends the summary to Claude asking for key action items as JSON
  b) Print the intermediate summary and the final extracted action items
  c) Track total tokens used across both calls
```

**Day 2 — Build: Daily Briefing Generator**

Build with Claude Code:
> "Build a daily briefing generator. It should: take a list of mock emails (as JSON) and mock calendar events (as JSON), use prompt chaining to first prioritize the emails then summarize the day's schedule, and produce a formatted morning briefing. Use list comprehensions where appropriate."

**Day 3 — Extend + Commit:**
- Add a feature yourself: let the user specify a "focus area" that influences how emails are prioritized
- Commit with Git branching

---

### Week 5: CSV Data and the Finance Analyzer

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write a list comprehension that extracts names from a list of student dicts where grade > 80.

New Python concepts: CSV module, while loops, data validation

```
Exercise 33: CSV reading/writing —
  a) Create a CSV file with 10 mock transactions (date, description, amount, category)
  b) Read it with csv.DictReader and print headers + first 5 rows
  c) Write a filtered version (only transactions > $50) to a new CSV file

Exercise 34: While loops —
  a) Write a retry pattern: call a function that randomly fails, retry up to 3 times
  b) Write a simple menu loop: show options, get input, execute, repeat until user quits
  c) Why this matters for agents: an agent loop is fundamentally a while loop —
     "keep going until the task is done or you hit a limit"

Exercise 35: Data analysis functions —
  a) Given a list of transaction dicts, write functions for: total spending, 
     spending per category, daily average, top 5 largest transactions
  b) Write a function that groups uncategorized transactions using simple keyword matching
     (e.g., "Uber" or "Lyft" → "Transport", "Starbucks" or "restaurant" → "Food")
```

New AI concept: **Batch API calls and data validation** — calling Claude for each item in a dataset, validating responses, handling failures gracefully.

```
Exercise 36: Batch categorization —
  a) Write a function that takes a list of uncategorized transactions
  b) For each one, call Claude to categorize it (structured JSON output)
  c) Collect results, handle any failed calls, report success rate
  d) Compare: Claude's categorization vs. your keyword-matching function from Exercise 35
```

**Day 2 — Build: Personal Finance Analyzer**

Build with Claude Code:
> "Build a finance analyzer. It reads a CSV of transactions, uses Claude to categorize uncategorized ones, calculates spending summaries per category, and generates a report. Include data validation, batch API error handling, and both JSON and text output."

**Day 3 — Extend + Commit:**
- Add a feature yourself: monthly trend comparison (if the CSV has multiple months)
- Commit with Git branching

---

### Week 6: Text Chunking and the Research Synthesis Assistant

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write a while loop that keeps asking for input until the user types "quit".

New Python concepts: String slicing for chunking, working with multiple files, tuples

```
Exercise 37: Text chunking —
  a) Write a function split_into_chunks(text, chunk_size=500, overlap=50) that splits
     text into chunks of roughly chunk_size words, with overlap words carried over
  b) Test it on a long text and verify: chunks overlap correctly, no words are lost
  c) Why this matters: documents are often too long for a single API call. Chunking
     is the foundation of RAG and multi-document processing.

Exercise 38: Multi-document processing —
  a) Write a function that reads all .txt files from a folder and returns a list of
     dicts with "filename", "content", and "word_count"
  b) Write a function that takes multiple summaries and builds a "synthesis prompt" —
     asking Claude to combine them into one coherent briefing

Exercise 39: Tuples —
  a) Write a function that returns multiple values as a tuple: (min, max, average)
  b) Unpack the tuple into separate variables
  c) When to use tuples vs. lists vs. dicts (quick comparison)
```

New AI concept: **Multi-document processing** — summarizing multiple documents individually, then synthesizing across them. This is the pattern behind research assistants and is a stepping stone to RAG.

**Day 2 — Build: Research Synthesis Assistant**

Build with Claude Code:
> "Build a research synthesis tool. It reads multiple text files from a folder, summarizes each one individually, then synthesizes all summaries into a single coherent briefing with key themes, contradictions, and recommendations. Use text chunking for long documents."

**Day 3 — Extend + Commit:**
- Add a feature yourself: generate a "questions for further research" section based on gaps in the synthesis
- Commit with Git branching

---

### Week 7: MCP Foundations + Claude Code Skills

**Day 1 — MCP Conceptual Foundation + Claude Code Skills:**

Warm-up: Write a text chunking function from memory (reinforces Week 6).

**MCP Deep Dive (conceptual):**
- What problem MCP solves: the "N×M integration problem" — before MCP, every AI app needed custom code for every tool
- Architecture: Host (AI app) → Client (connector) → Server (tool/data provider)
- The three things MCP servers expose: **Tools** (actions), **Resources** (data), **Prompts** (templates)
- Transport: JSON-RPC 2.0 over stdio (local) or HTTP (remote)
- Real-world example walkthrough: how Claude Desktop connects to Gmail via MCP
- MCP vs. function calling: MCP standardizes what function calling does, making it universal across models
- MCP vs. RAG: RAG fills the model's context window; MCP connects the model to the real world. They complement each other.
- Security considerations: permissions, OAuth 2.1, what data the AI can access

```
Exercise 40: MCP architecture quiz (answer in a text file, commit to Git) —
  a) Draw (in text/ASCII) the MCP architecture for this scenario: 
     Claude Desktop needs to read your Gmail and check your Google Calendar
  b) Label: host, clients, servers, tools exposed by each server
  c) Explain: why does the host create one client per server, not one client for all?
  d) When would you build your own MCP server vs. use an existing one?
```

**Claude Code Skills — Introduction:**
- What a skill is: a SKILL.md file with YAML frontmatter + markdown instructions
- Progressive disclosure: metadata (always loaded, ~100 tokens) → full instructions (loaded when triggered, <5k tokens) → bundled resources (loaded when needed)
- Three patterns: reference content (conventions, style guides), task content (step-by-step workflows), forked context (run in a subagent)
- When to use a skill vs. a regular prompt vs. CLAUDE.md instructions

```
Exercise 41: Create your first Claude Code skill —
  a) Create a skill that helps you set up a new exercise file:
     ~/.claude/skills/new-exercise/SKILL.md
     - Creates the file in the right folder with proper naming
     - Adds a header comment with date, exercise number, topic
     - Adds a basic structure (imports, main function, if __name__ block)
  b) Write proper YAML frontmatter (name, description)
  c) Test it: invoke with /new-exercise in Claude Code
  d) Iterate: refine based on output quality
```

**Day 2 — Hands-On: MCP in Claude Desktop + Skills Practice**

MCP hands-on — connect and test these specific services:
- **Gmail MCP connector:** Connect → ask Claude to summarize your 5 most recent emails → observe what tools it calls
- **Google Calendar MCP connector:** Connect → ask Claude to show today's schedule → observe the request/response flow
- **Observe the pattern:** Claude decides which MCP tool to call based on your request, executes it, reads the result, and responds. This is tool calling happening live — the same pattern you'll build from scratch in Week 8.

Skills practice:
- Create a second skill: a /wrap-up skill that helps generate end-of-session documentation updates
- Test both skills in your actual workflow

**Day 3 — Revisit Daily Briefing + Commit**

- Take your Week 4 Daily Briefing project and discuss: how would this change with real data via MCP?
- What changes: authentication, rate limits, data format variability, error handling, privacy
- What stays the same: prompt chaining, prioritization logic, output formatting
- Update all tracking documents
- Commit skills and notes to Git

**Phase 2 Checkpoint:** You can build multi-step AI tools that process CSV data, chain API calls, handle batches, chunk long documents, and synthesize across multiple sources. You understand MCP architecture conceptually and have used MCP connectors hands-on. You can create Claude Code skills to customize your workflow.

---

## Phase 3: Agents, Tool Calling, and the AI Stack (Weeks 8-11)

**Goal:** Understand how AI agents work from the inside. Build agents that use tools, manage state, delegate to sub-agents, and make decisions. Understand RAG, embeddings, and when to use each AI approach. Fine-tune a model. By the end of this phase, you can architect AI systems, not just build scripts.

**Phase 3 ordering rationale:** Tool calling and agents come first (Weeks 8-9) because they're the highest priority and the foundation for everything else. RAG follows (Week 10) because it's a technique agents *use*. Sub-agents and fine-tuning close the phase (Week 11) as advanced extensions.

### Week 8: Tool Calling, Multi-Turn Conversations, and Your First Agent

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write a prompt chaining function from memory (reinforces Week 4).

New AI concepts: **Multi-turn conversation management** — building a chatbot that maintains history across API calls. This is the bridge between single API calls and agent loops. **Tool calling / function calling** — giving Claude the ability to *do things*, not just talk.

```
Exercise 42: Multi-turn conversations via the API —
  a) Write a simple chatbot:
     - Maintain a messages list: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
     - Each turn: append the user's message, call Claude with the full history, append Claude's response
     - Loop until the user types "quit"
  b) Print the full conversation history at the end
  c) Add token tracking: how many tokens does the conversation use as it gets longer?
  d) Why this matters: an agent loop is a multi-turn conversation where some "turns" 
     are tool calls instead of user messages.

Exercise 43: Tool calling basics —
  a) Define 3 simple Python functions:
     - get_weather(city) → returns mock weather data as a dict
     - calculate(expression) → evaluates a math expression safely
     - get_current_time(timezone) → returns current time as a string
  b) Create tool definitions for Claude's API (name, description, input_schema for each)
  c) Send a message to Claude with these tools defined
  d) Parse Claude's response: did it want to call a tool? Which one? With what arguments?
  e) Execute the tool, send the result back as a tool_result message, get Claude's final answer
  f) Handle the case where Claude calls multiple tools in one turn

Exercise 44: The agent loop —
  a) Wrap Exercise 43 in a while loop: keep calling Claude until it gives a final
     text response (no more tool calls)
  b) Add a max_iterations limit (prevent infinite loops)
  c) Print each step: what Claude decided, what tool was called, what result came back
  d) This IS an agent. An LLM in a loop with tools.
```

**Day 2 — Build: Simple Tool-Using Agent**

Build with Claude Code:
> "Build a simple agent that can answer questions using tools. Give it these tools: search_notes (searches a folder of text files by keyword and returns matching excerpts), calculate (evaluates math expressions), summarize_text (sends text to Claude for summarization), and save_result (saves output to a file). The agent should handle multi-step requests like 'Find my notes about Python functions, summarize them, and save the summary.' Include step-by-step logging of the agent's decisions."

Evaluation (woven into the build):
> Define 5 test tasks for your agent. Run each one. Record: did it complete the task? How many steps did it take? Did it use the right tools? Did it recover from any errors? Save results as a test_results.json file.

**Day 3 — Extend + Commit:**
- Add a feature yourself: a "think out loud" mode that prints the agent's reasoning at each step
- Add error recovery: if a tool call fails, the agent should retry or try a different approach
- Commit with Git branching

---

### Week 9: Agent Patterns — State, Error Recovery, and Human-in-the-Loop

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write the tool-calling agent loop pattern from memory (while loop + tool execution + history management).

New AI concepts: **State management** — tracking what an agent has done, what's left, and carrying context forward. **Human-in-the-loop** — designing agents that pause for approval at critical steps. **Error recovery** — what happens when things fail mid-workflow.

```
Exercise 45: State management with classes —
  a) Create a TaskState class that tracks:
     - current_step (string)
     - completed_steps (list)
     - results (dict mapping step names to outputs)
     - errors (list of error messages)
     - status ("running", "paused", "completed", "failed")
  b) Add methods: mark_complete(step, result), record_error(step, error), to_dict()
  c) Pass this state through an agent workflow — the agent updates state at each step

Exercise 46: Human-in-the-loop pattern —
  a) Build an agent that processes a list of items but pauses for user approval
     before any "destructive" action (e.g., saving a file, sending a message)
  b) The agent presents what it wants to do, waits for yes/no, then proceeds or skips
  c) Why this matters: in production, agents that auto-execute everything are dangerous.
     The approval pattern is how you build trust.

Exercise 47: Error recovery pattern —
  a) Build an agent that can handle tool failures:
     - If a tool call fails, try an alternative approach
     - If all approaches fail, report the error and continue with remaining tasks
     - Never crash — always degrade gracefully
  b) Test by intentionally breaking a tool (e.g., searching for a file that doesn't exist)
```

**Day 2 — Build: Robust Task Execution Agent**

Build with Claude Code:
> "Build an agent that takes a complex multi-step task (like 'Research topic X, create a summary, and prepare an email draft'), breaks it into steps, executes each step with appropriate tools, tracks state throughout, handles errors gracefully, and pauses for human approval before any output-producing action. Use the TaskState class for state management."

Evaluation (woven into the build):
> Test the agent with 3 scenarios: a task that succeeds fully, a task where one step fails (simulate by giving an invalid file path), and a task where the user declines an approval. Record how the agent handles each case.

**Day 3 — Extend + Commit:**
- Add a feature yourself: a "resume" capability — if the agent stops mid-task, it can pick up from the last completed step by loading saved state
- Commit with Git branching

---

### Week 10: RAG — Retrieval-Augmented Generation

**Day 1 — Python Exercises + Concepts:**

Warm-up: Write the TaskState class from memory with mark_complete() and record_error() methods.

New AI concepts: **Embeddings** — turning text into numbers so you can measure similarity. **Vector search** — finding the most relevant chunks of text for a query. **RAG pipeline** — search first, then generate.

```
Exercise 48: Understanding embeddings —
  a) Use a simple embedding API or library to embed three sentences:
     - "The cat sat on the mat"
     - "A kitten rested on the rug"
     - "Python is a programming language"
  b) Compute cosine similarity between all pairs
  c) Verify: the two cat sentences should be more similar to each other than to Python
  d) Write your own cosine_similarity(vec_a, vec_b) function to understand the math

Exercise 49: Build RAG from scratch (keyword version first) —
  a) Take a collection of text chunks (from your Week 6 chunking function)
  b) Write a keyword search function: given a query, find the chunks with the most word overlap
  c) Build a RAG pipeline: query → search → inject top 3 chunks into a prompt → get answer
  d) Test with 5 questions about the source documents
  e) Record: did the answer use information from the retrieved chunks? Was it accurate?

Exercise 50: Upgrade to vector search —
  a) pip install chromadb
  b) Create a ChromaDB collection, add your chunks with embeddings
  c) Query the collection, get the top 3 most relevant chunks
  d) Compare answers: keyword RAG vs. vector RAG — which found better context?
  e) Evaluation: run the same 5 test questions through both systems, compare accuracy
```

**Day 2 — Build: Q&A Bot Over Your Own Documents**

Build with Claude Code:
> "Build a Q&A bot that answers questions about a folder of documents (e.g., your notes, MBA materials, or any text files). It should: chunk documents, store them in ChromaDB, retrieve relevant chunks for each question, and generate grounded answers with citations (which document and chunk the answer came from). Use the agent pattern from Week 8 — the RAG search is just another tool the agent can call."

Evaluation (built into the project):
> Create a test_questions.json with 10 questions and expected answers. Run each question through the bot. Score: correct, partially correct, or wrong. Calculate accuracy. Identify failure modes: is it a retrieval problem (wrong chunks found) or a generation problem (right chunks, wrong answer)?

**Day 3 — Extend + Commit:**
- Add a feature yourself: confidence scoring — when the retrieved chunks have low relevance scores, the bot should say "I don't have enough information" instead of guessing
- Run the 10 test questions again with confidence scoring and compare results
- Commit with Git branching

---

### Week 11: Sub-Agents, Fine-Tuning, and the Decision Framework

**Day 1 — Sub-Agent Patterns + Concepts:**

Warm-up: Build a mini RAG pipeline from memory (chunk → store in ChromaDB → search → answer).

New AI concepts: **Sub-agents** — specialized agents that a "manager" agent delegates to. **Why:** complex tasks benefit from specialization; each sub-agent has its own tools and system prompt.

```
Exercise 51: Sub-agent pattern —
  a) Write a "manager" function that takes a complex request and breaks it into sub-tasks
  b) Write two "worker" functions, each with their own system prompt and tools:
     - researcher(query) → searches files and returns findings (can use RAG)
     - writer(findings, format) → takes research and writes formatted output
  c) The manager calls researcher first, passes results to writer
  d) Compare: one monolithic prompt vs. the manager+worker chain — which gives better results?

Exercise 52: Delegation with state tracking —
  a) Extend the sub-agent pattern with TaskState:
     - Manager creates the plan and tracks overall state
     - Each sub-agent reports back its results and any errors
     - Manager decides next steps based on sub-agent results
  b) Add a case where the researcher doesn't find enough information and the manager
     asks for a different search approach
```

**Day 2 — Build: Research Team Agent**

Build with Claude Code:
> "Build a research agent that uses delegation. A manager agent receives a research question, creates a plan, then delegates to specialized sub-agents: a searcher (finds relevant documents using RAG from Week 10), an analyzer (extracts key findings and evaluates source quality), and a writer (synthesizes into a formatted briefing). Each sub-agent has its own system prompt and tools. The manager coordinates, handles errors, and compiles the final output with citations."

**Day 3 — Fine-Tuning + The Decision Framework:**

**The Decision Framework — when to use what:**

```
PROMPTING ALONE
  When: Task is well-defined, model already knows the domain, output format is flexible
  Cost: Lowest (just API calls)
  Example: Summarizing emails, drafting messages, answering general questions

PROMPTING + RAG
  When: Task requires specific knowledge the model doesn't have (company docs, recent data)
  Cost: Low-medium (API calls + embedding/storage)
  Example: Q&A over internal documents, customer support with product knowledge base

FINE-TUNING
  When: Model needs to learn a specific style, format, or domain that prompting can't capture
  Cost: High (dataset preparation, training compute, ongoing maintenance)
  Example: Medical report generation in a specific format, legal document analysis
  Note: Applicable to open-source models (Llama, Mistral). Anthropic doesn't offer fine-tuning for Claude.

LoRA (Low-Rank Adaptation)
  When: Same as fine-tuning but you want it cheaper and faster
  Cost: Medium (smaller dataset, less compute than full fine-tune)
  Example: Adapting an open-source model to your company's writing style

CUSTOM/TRAINED MODEL
  When: Completely novel task that no existing model handles
  Cost: Highest (data collection, training infrastructure, ongoing maintenance)
  Almost never the right choice for text-based enterprise AI.
```

**Hands-on: Hugging Face + Fine-Tuning Exercise**

```
Exercise 53: Explore Hugging Face —
  a) Browse huggingface.co — find 3 interesting datasets and 3 interesting models
  b) pip install transformers datasets
  c) Load a small dataset from Hugging Face (e.g., a sentiment analysis dataset)
  d) Load a small pre-trained model and run inference on a few examples
  e) Document: what's in the dataset? How is the model structured?

Exercise 54: Fine-tune a small model with LoRA —
  a) Choose a small model (e.g., a tiny GPT-2 or small Llama variant)
  b) Prepare a small dataset (can be synthetic — e.g., 100 examples of a specific writing style)
  c) Fine-tune using LoRA (with the PEFT library from Hugging Face)
  d) Compare: original model output vs. fine-tuned output on the same prompts
  e) Document: what changed? How much data did it take? Was the improvement worth the effort?
  f) Reflect: based on this experience, when would you recommend fine-tuning to a client vs. RAG?
  Note: Use Google Colab or Kaggle Notebooks for free GPU access.
```

**Phase 3 Checkpoint:** You understand how agents work (tool calling, loops, state, delegation). You've built RAG from scratch and can evaluate it. You've fine-tuned a model and understand when it's worth it. You can advise clients on which AI approach to use and explain why. You understand the full AI stack.

---

## Phase 4: The Anthropic Ecosystem Deep Dive (Weeks 12-14)

**Goal:** Master the tools in the Anthropic ecosystem — advanced Claude Code skills, subagents, MCP server creation, Cowork, and Agent Teams. By the end, you can create custom AI workflows that automate real tasks and integrate with external services.

### Week 12: Advanced Claude Code — Subagents and Skill Patterns

**Day 1 — Concepts + Exercises:**

Warm-up: Write the sub-agent delegation pattern from memory (manager → researcher → writer).

**Claude Code Subagents:**
- What they are: helper agents spawned within a Claude Code session for focused tasks
- When to use: research, verification, code review — tasks that benefit from a fresh context
- How they work: the main agent creates a task, a subagent runs it in isolation, returns results
- Limitations: can't spawn their own subagents, report back to main agent only, no inter-agent communication
- The "context: fork" pattern in SKILL.md — skills that run in a subagent

```
Exercise 55: Advanced skill creation —
  a) Create a skill with "context: fork" that researches a topic in your codebase:
     ~/.claude/skills/code-research/SKILL.md
     - Uses the Explore agent type for read-only codebase exploration
     - Takes a topic as $ARGUMENTS
     - Returns a summary of relevant files and patterns
  b) Create a task-oriented skill that automates a multi-step process:
     e.g., /review-exercise that checks your latest exercise file for common patterns,
     suggests improvements, and verifies it runs without errors
  c) Test both skills in real workflows

Exercise 56: Skill composition —
  a) Create a skill that uses information from your CLAUDE.md and your config patterns
  b) Test: does Claude Code combine skill instructions with project context correctly?
  c) Experiment: what happens when two skills might both apply? How does Claude choose?
```

**Day 2 — Build: Your Custom Development Toolkit**

In Claude Code:
> "Help me create a complete set of Claude Code skills for my ai-builder project: (1) /new-exercise — creates a properly structured exercise file, (2) /test-it — runs the current Python file and provides helpful error analysis, (3) /code-review — analyzes code for patterns I've learned and suggests improvements, (4) /wrap-up — generates end-of-session documentation updates. Each should have proper YAML frontmatter and clear instructions."

**Day 3 — Extend + Commit:**
- Create one more skill yourself: a /explain skill that takes a code file and generates a beginner-friendly walkthrough
- Test all skills across several workflows
- Commit everything

---

### Week 13: Building MCP Servers + Cowork

**Day 1 — MCP Server Creation:**

Warm-up: Describe the MCP architecture from memory (host → client → server → tools/resources/prompts).

**Building Your Own MCP Server:**
- When you'd build one: you have a tool/API/database that you want any AI app to access
- Anatomy of an MCP server: tool definitions, resource definitions, handler functions
- The Python SDK for MCP: `pip install mcp`
- Transport: stdio for local servers, HTTP for remote servers
- Testing with the MCP Inspector tool

Concrete project — **wrap your Meeting Notes Processor as an MCP server:**

```
Exercise 57: Build an MCP server —
  a) Create an MCP server that exposes two tools:
     - process_meeting_notes(transcript_path) → runs your meeting notes processor, 
       returns the structured JSON result
     - search_meeting_history(query) → searches your output folder for past meeting
       notes containing the query
  b) Add one resource: expose your most recent meeting summary as a readable resource
  c) Register the server with Claude Desktop
  d) Test: ask Claude Desktop "What were the action items from my last meeting?" 
     — it should use your MCP server

Exercise 58: Extend the MCP server —
  a) Add a third tool: generate_follow_up(meeting_id) → creates a follow-up email
     from a specific meeting's processed notes
  b) Test the full flow in Claude Desktop: process notes → search history → generate follow-up
  c) Observe: Claude chains your MCP tools the same way it chains built-in tools
```

**Day 2 — Cowork Deep Dive:**

**Cowork concepts:**
- How Cowork differs from Claude Code: GUI vs terminal, same agentic architecture underneath
- Projects: persistent workspaces with files, instructions, and task history
- Plugins: bundles of skills + connectors + sub-agents packaged for specific workflows
- Scheduled tasks: recurring automation (daily briefings, weekly reports)
- Dispatch: control Cowork from your phone while it runs on your desktop

**Hands-on in Cowork:**
- Create a Cowork project for "Document Processing"
- Point it at a folder with various files
- Task: "Organize these documents, create a summary index, and flag any that need follow-up"
- Observe: how does Cowork plan, execute, and report progress?
- Try connecting your custom MCP server — can Cowork use your search_meeting_history tool?
- If your plan supports it: set up a scheduled task

**Day 3 — Extend + Commit:**
- Document: comparison of Claude Code vs. Cowork for your workflows — when would you use each?
- Test your MCP server from both Claude Desktop and Cowork
- Commit everything

---

### Week 14: Agent Teams + Capstone Project

**Day 1 — Agent Teams Concepts + Exploration:**

Warm-up: Create a simple SKILL.md from memory with proper YAML frontmatter.

**Claude Code Agent Teams (experimental):**
- What they are: multiple Claude Code sessions working together with a shared task list
- Architecture: one lead + multiple teammates, each with their own context window
- Communication: teammates can message each other and the lead directly
- Task management: shared task list with claiming, completion tracking, and handoffs
- When to use: tasks that benefit from parallel work (research different aspects simultaneously, build separate components)
- When NOT to use: sequential tasks, same-file edits, simple projects (coordination overhead not worth it)
- Subagents vs. Agent Teams: subagents are "contractors sent on separate errands," teams are "a project team in the same room coordinating actively"
- Token cost reality: Agent Teams use significantly more tokens than single sessions

**Exploration (if available on your plan):**
- Try a simple Agent Team setup: one lead + one teammate working on different files
- Observe: how do they communicate? How does the lead assign and track tasks?

**Day 2-3 — Capstone Integration Project**

This is the project that brings together everything from Phases 2-4. Choose one:

**Option A: Enterprise Knowledge Assistant**
> An agent that searches your documents (RAG), uses MCP to access external data, delegates to sub-agents for specialized tasks (analysis, writing), and produces formatted reports. Uses your custom Claude Code skills for workflow automation. Includes state management and error recovery.

**Option B: Automated Research Pipeline**
> Given a research topic, the system: searches local documents (RAG), delegates analysis to sub-agents, synthesizes findings, and generates a polished brief with citations and confidence scores. Can be triggered as a Claude Code skill or run through Cowork.

**Option C: Personal Productivity System**
> Combines email briefing (Week 4), document search (RAG), and task management. Uses MCP for Gmail/Calendar, your custom MCP server for meeting notes, and agents for prioritization and summarization. Produces a daily action plan.

Build over 2 days:
- Day 2: Plan architecture in Claude Chat, build core with Claude Code
- Day 3: Test with evaluation criteria (define 5 test scenarios, record results), polish, add documentation and README, commit final version

Evaluation for the capstone:
> Define 5 realistic test scenarios. For each: describe the input, expected behavior, and success criteria. Run all 5, record results. Document: what worked, what failed, what you'd improve with more time.

**Phase 4 Checkpoint:** You can create Claude Code skills and subagents, build MCP servers, use Cowork for automation, and understand Agent Teams. You've built a capstone project that integrates agents, RAG, tools, and MCP. You can create custom AI workflows end-to-end.

---

## Phase 5: Consulting Toolkit + Foundations for Startup (Weeks 15-17)

**Goal:** Package everything you've learned into reusable consulting assets. Build the materials you'd use to advise enterprise clients on AI strategy. Deploy one tool.

### Week 15: The Consulting Toolkit

**Deliverables to create:**

1. **AI Approach Decision Framework** (one-pager)
   - When to use: prompting, RAG, fine-tuning, LoRA, custom training, agents, MCP
   - Cost/timeline/complexity comparison table
   - Decision tree for non-technical executives
   - Based on your hands-on experience — include specific examples from your projects

2. **AI Readiness Assessment** (questionnaire)
   - Questions to assess a company's readiness for AI implementation
   - Sections: data readiness, process documentation, technical infrastructure, change management, budget
   - Scoring rubric with recommendations per tier

3. **Scoping Document Template**
   - Template for scoping an AI project for a client
   - Sections: problem statement, proposed approach, data requirements, architecture, timeline, cost estimate, risks, success metrics

4. **Demo Portfolio**
   - Your best 3-4 projects cleaned up and documented
   - Each with: what it does, what AI approach it uses, why that approach, what it cost (tokens), how it's evaluated
   - Runnable demos a client could see

### Week 16: Deployment Basics

- **Streamlit** — give one of your agents a simple web UI that someone else could use
- **Hosting** — Railway or Render for a simple deployment
- **Secrets management** — environment variables in production vs. local development
- **Logging** — tracking what your agent does, when, and at what cost

### Week 17: Reflect and Plan Forward

- Review everything you've built
- Identify the 3 strongest projects for your portfolio
- Plan your post-roadmap learning path (LangChain, CrewAI, advanced deployment, Docker, n8n for client delivery, etc.)
- Consider: what would you build for your first consulting client? What would you build for your startup?

---

## Reference: Python Concepts by Phase

### Phase 1 (Complete) ✅
Variables, types, strings, f-strings, lists, dictionaries, functions, default arguments, conditionals, for loops, file I/O, JSON, enumerate, error handling (try/except), imports, pip, environment variables, HTTP requests, Anthropic SDK, classes (basic), argparse, multi-file projects, structured outputs, .join(), string building (+=), .get() for safe access

### Phase 2 (Weeks 4-7)
List comprehensions, datetime module, sorting with key functions, while loops, CSV reading/writing, tuples, text chunking, multi-document processing, prompt chaining, batch API calls, data validation

### Phase 3 (Weeks 8-11)
Multi-turn conversation history management, tool calling API pattern (tool definitions, tool_use responses, tool_result messages), agent loop (while + tool calls + history), state management with classes, human-in-the-loop approval patterns, error recovery patterns, cosine similarity, embeddings, ChromaDB, RAG pipeline, sub-agent delegation, Hugging Face transformers/datasets, PEFT/LoRA basics

### Phase 4 (Weeks 12-14)
Advanced SKILL.md patterns (context: fork, agent types, $ARGUMENTS), MCP Python SDK, MCP server tool/resource definitions, Claude Code subagents, Agent Teams concepts

---

## Reference: AI Concepts by Phase

### Phase 1 (Complete) ✅
What an API is, HTTP GET requests, status codes, JSON as API language, system prompts vs user messages, token counting, structured outputs, defensive JSON parsing

### Phase 2 (Weeks 4-7)
Prompt chaining, multi-document synthesis, batch processing, text chunking (pre-RAG skill), MCP architecture (conceptual: host/client/server, tools/resources/prompts, transport), Claude Code skills (SKILL.md, YAML frontmatter, progressive disclosure)

### Phase 3 (Weeks 8-11)
Multi-turn conversation management, tool calling / function calling (the mechanism that makes agents possible), agent loops (observe → think → act → repeat), state management, error recovery, human-in-the-loop, embeddings and vector search, RAG pipeline (chunk → embed → store → search → generate), retrieval evaluation (precision, accuracy), sub-agent delegation (manager → specialist workers), fine-tuning vs. LoRA, Hugging Face ecosystem, the AI decision framework (prompting → RAG → fine-tuning → custom)

### Phase 4 (Weeks 12-14)
Claude Code subagents (context: fork, Explore agent), advanced skills composition, MCP server creation (Python SDK, tool definitions, resource exposure, testing), Cowork (projects, plugins, scheduled tasks, Dispatch), Agent Teams (lead/teammate model, shared task lists, communication patterns), capstone integration (agents + RAG + MCP + skills)

---

## Reference: The Session Handoff Block

Template (paste at the start of each session):
```
SESSION HANDOFF — [date]
Last session: [what we covered]
Current position in roadmap: [phase/week/day]
What I built: [files/scripts]
What I'm stuck on: [if anything]
Python skills current level: [recent additions]
Next planned topic: [from roadmap]
Goal for this session: [what I want to accomplish]
```

---

## Reference: Tools and Their Roles

**Claude Chat (this Project):** Primary teacher. Concepts, exercises, architecture discussions, code review, planning before builds.

**Claude Code (VS Code terminal):** Building partner. Writes code you review, runs scripts, manages files. Always launch from project folder. Custom skills extend its capabilities.

**VS Code:** Reading/editing code. Running exercises by hand. Seeing project structure.

**Git + GitHub:** Save points for every working version. Safety net for rollbacks. Portfolio proof.

**Claude Desktop / Cowork:** MCP connections to external services. Desktop automation and scheduled tasks (Phase 2 introduction, Phase 4 deep dive).

**Hugging Face:** Model and dataset hub for fine-tuning exercises (Phase 3).

**Google Colab / Kaggle Notebooks:** Free GPU access for fine-tuning (Phase 3).

**ChromaDB:** Local vector database for RAG (Phase 3).

**Streamlit:** Simple web UI for deploying tools (Phase 5).

---

## Glossary

**Agent:** An LLM in a loop that can observe, think, and act. The core pattern: receive task → plan → use tools → check result → repeat or finish.

**Agent Team:** Multiple Claude Code sessions working together with a shared task list and direct messaging. One leads, others work independently. Experimental feature.

**Cosine Similarity:** A mathematical measure of how similar two vectors (lists of numbers) are. Used to compare embeddings and find related text.

**Cowork:** Claude Code's agentic architecture with a GUI, for non-coding desktop tasks. Runs in Claude Desktop.

**Dispatch:** Feature that lets you control Cowork from your phone while it works on your desktop.

**Embedding:** A numerical representation of text (a list of numbers). Similar texts get similar numbers. Used for search and RAG.

**Evaluation:** Testing whether your AI system works correctly. For RAG: test questions with known answers. For agents: test tasks with success criteria. Simple but essential.

**Fine-tuning:** Retraining an existing model on your specific data. Changes the model's behavior permanently. Expensive. Usually unnecessary when prompting + RAG works.

**Human-in-the-Loop:** An agent design pattern where the agent pauses for human approval before taking critical actions. Builds trust and prevents errors.

**LoRA (Low-Rank Adaptation):** A cheaper way to fine-tune by only updating a small portion of the model's parameters. Works on open-source models (Llama, Mistral).

**MCP (Model Context Protocol):** An open standard for connecting AI apps to external tools and data. Architecture: Host → Client → Server. Servers expose tools, resources, and prompts.

**MCP Server:** A program that exposes tools/data to AI apps via the MCP standard. You can use pre-built ones (Gmail, Calendar) or build your own.

**Multi-Turn Conversation:** A conversation where the full message history is sent with each API call, allowing the model to reference earlier messages. Foundation for agent loops.

**Prompt Chaining:** Breaking a complex task into sequential LLM calls where each output feeds the next.

**RAG (Retrieval-Augmented Generation):** Search for relevant documents first, then send them to the AI with your question. Lets AI answer about specific data it wasn't trained on.

**Skill (Claude Code):** A SKILL.md file with YAML frontmatter and markdown instructions that extend Claude Code's capabilities. Invoked with /skill-name or triggered automatically.

**State Management:** Tracking what an agent has done, what's left, any errors, and any accumulated context. Usually implemented with a class like TaskState.

**Subagent:** A helper agent spawned within a Claude Code session for a focused task. Reports results back to the main agent. Can't spawn its own subagents.

**Tool Calling / Function Calling:** The mechanism where an LLM decides which tools (Python functions) to call based on a request. Your code executes the function and returns the result. The foundation of agents.

**Vector Database:** A database optimized for storing and searching embeddings. ChromaDB (local), Pinecone (cloud).
