# AI Builder Roadmap v2 — Complete Plan

## Pablo's Profile

- MIT MBA student, 5 years startup experience (property, energy, back-office ops)
- Strong prompt engineering (built negotiation agents, customer support agents, system prompts with phased strategies)
- Beginner coder: Python ~3/10, can read/edit simple scripts, used n8n/Make
- Tools installed: Claude Code (ran a few commands), VS Code (never used seriously), GitHub account (never used)
- Weekly time: 5-8 hours in dedicated blocks, occasional longer weekend sessions
- Priority stack: Personal productivity tools → AI consulting for enterprises → AI-native B2B startup
- Industries: Energy operations, back-office automation, enterprise (McKinsey-tier use cases)
- Learning style: Wants structured Python exercises before building, prefers understanding before doing, reviews proposed changes before approving

---

## Part 1: Architecture — How Everything Connects

### The Problem This Solves

AI learning breaks down when you lose context across sessions. You build something in Week 2, then in Week 5 you can't remember how it worked, Claude doesn't know what you already tried, and you waste time re-explaining your level and preferences. This architecture prevents that.

### The Three Layers

```
LAYER 1 — KNOWLEDGE & PROGRESS (Claude Projects)
  What: Roadmap, progress log, session summaries, learning preferences
  Where: One master Claude Project called "AI Builder — Learning"
  Why: Claude automatically sees this in every conversation
  
LAYER 2 — CODE (Git + VS Code + Claude Code)
  What: All scripts, projects, experiments
  Where: Git repos on GitHub, accessed via VS Code + Claude Code
  Why: Version-controlled, rollback-safe, Claude Code reads directly

LAYER 3 — LEARNING ARTIFACTS (Saved files + bookmarks)
  What: Interactive lessons, apps, visualizations created during learning
  Where: Saved as files in a dedicated folder, linked from progress log
  Why: Revisitable without rebuilding
```

### How The Tools Connect

```
┌─────────────────────────────────────────────────┐
│              YOUR LEARNING SESSION               │
│                                                  │
│  1. Open Claude Project "AI Builder — Learning"  │
│  2. Paste your Session Handoff Block (see below) │
│  3. Learn concept + do Python exercises          │
│                                                  │
│  When ready to build:                            │
│  4. Open VS Code → open project folder           │
│  5. Launch Claude Code in VS Code terminal        │
│  6. Build with Claude Code as coding partner      │
│  7. Commit working code to Git                   │
│                                                  │
│  End of session:                                 │
│  8. Update Session Handoff Block                 │
│  9. Upload updated progress log to Project       │
└─────────────────────────────────────────────────┘
```

### Tool Roles

**Claude Chat (within your "AI Builder — Learning" Project)**
- Primary teacher for concepts and Python exercises
- Architecture discussions and design decisions
- Reviewing and explaining code before you build
- Debugging when Claude Code gets stuck
- NOT for active coding (that's Claude Code)

**Claude Code (inside VS Code terminal)**
- Your coding partner — describe what you want, it writes code
- Reads your project files and understands the codebase
- Runs scripts, installs packages, manages files
- You review everything before approving
- ALWAYS launched from a specific project folder, never from home directory

**VS Code**
- Reading and editing code that Claude Code generates
- Seeing your project file structure
- Running Claude Code in the integrated terminal
- The place where you manually edit code for Python exercises

**Git + GitHub**
- Save points for every working version of your code
- Safety net: if Claude Code breaks something, you roll back
- Portfolio: your GitHub becomes proof of what you've built
- One repo per project

**Claude Projects (the knowledge layer)**
- Upload: this roadmap, your progress log, your preferences doc
- Custom instructions: your learning context and rules for Claude
- Every conversation in this Project automatically has your full context
- When you start a new chat in the Project, Claude already knows where you are

### Setting Up Your Claude Project — Step by Step

**Step 1: Create the Project**
- Go to claude.ai → Projects (left sidebar) → Create Project
- Name: "AI Builder — Learning"
- Description: "Pablo's AI engineering learning journey. Roadmap, progress, exercises, and build projects."

**Step 2: Set Custom Instructions**
Paste this into the Project Instructions field:

```
You are Pablo's AI engineering teacher. 

CONTEXT:
- Pablo is an MIT MBA student learning to build AI tools
- He is a beginner coder (Python ~3/10) but has strong analytical skills and prompt engineering experience
- He wants to understand concepts before building
- He prefers structured Python exercises before tackling projects
- He reviews proposed changes before approving them

TEACHING RULES:
1. Teach one concept at a time
2. Always provide a Python exercise for new concepts BEFORE using them in a project
3. Explain WHY something works, not just how
4. When showing code, explain each new element
5. Never introduce a new framework or tool unless the current project requires it
6. Connect every concept to a practical use case

SESSION STRUCTURE:
- Start by reading the Session Handoff Block the user pastes
- Confirm where we are in the roadmap
- Teach the planned concept with exercises
- End every session with:
  a) What we covered
  b) What was built or practiced
  c) One small exercise to do independently
  d) Updated Session Handoff Block for next time

IMPORTANT:
- If Pablo asks to build something, first check if the prerequisite Python concepts have been covered
- When he's ready to code in Claude Code, help him plan the approach HERE first, then he'll execute in Claude Code
- Keep track of which Python concepts he's comfortable with vs. still learning
```

**Step 3: Upload These Documents**
Upload to the Project Knowledge section:
1. This roadmap document (the file you're reading now)
2. Your Progress Log (template below — create it, then upload)
3. Your Python Skills Tracker (template below)

### The Progress Log — Template

Create this as a text file and upload it to your Project. Update it weekly.

```
# Progress Log — AI Builder Journey

## Current Status
- Current phase: Phase 0 — Setup & Orientation
- Current week: Week 0
- Last session date: [date]
- Next planned topic: Claude Code orientation
- Biggest blocker: None yet

## Completed
(Update as you go)
- [ ] Phase 0: Claude Code orientation
- [ ] Phase 0: Safety setup
- [ ] Phase 0: VS Code integration
- [ ] Week 1: Python basics — variables, types, strings
- [ ] Week 1: Python basics — lists, dictionaries
- [ ] Week 1: Python basics — functions, loops
- [ ] Week 1: Python basics — file I/O, JSON
- [ ] Week 1: Project — Text File Analyzer
...

## Session Summaries
### Session 1 — [date]
- Topic: 
- What I built/practiced:
- Key takeaway:
- Still confused about:
- Next step:
```

### The Python Skills Tracker — Template

```
# Python Skills Tracker

## Comfortable (can write from memory)
- (none yet)

## Familiar (can read and modify, need reference for writing)
- (none yet)

## Introduced (have seen it, need full guidance)
- (none yet)

## Not Yet Covered
- Variables and data types
- Strings and string methods
- Lists and list methods
- Dictionaries
- Tuples and sets
- Conditional statements (if/elif/else)
- For loops
- While loops
- List comprehensions
- Functions (defining, parameters, return values)
- Default arguments and keyword arguments
- Reading files
- Writing files
- JSON reading and writing
- CSV reading and writing
- Error handling (try/except)
- Importing modules
- Installing packages (pip)
- Environment variables
- Classes and objects (basic)
- HTTP requests
- API calls
- Working with dates/times
- String formatting (f-strings)
- Regular expressions (basic)
- Command line arguments
```

### The Session Handoff Block

This is a short text block you update at the end of every session and paste at the start of the next one. It's your "quick context injection" on top of the persistent Project knowledge.

Template:
```
SESSION HANDOFF — [date]
Last session: [what we covered]
Current position in roadmap: [phase/week]
What I built: [files/scripts]
What I'm stuck on: [if anything]
Python skills current level: [list recent additions]
Next planned topic: [from roadmap]
Goal for this session: [what I want to accomplish]
```

Example:
```
SESSION HANDOFF — March 15, 2026
Last session: Completed Python exercises on dictionaries and functions. Built a word frequency counter.
Current position in roadmap: Phase 1, Week 1, Day 3
What I built: word_counter.py in ai-learning repo
What I'm stuck on: Not sure when to use a list vs. a dictionary
Python skills current level: Variables, strings, lists (familiar), dictionaries (introduced), functions (introduced)
Next planned topic: File I/O and JSON
Goal for this session: Learn to read/write files, then start the Text File Analyzer project
```

---

## Part 2: Claude Code — Security, Permissions, and Safe Usage

### What Claude Code Can Do
- Read all files in the folder where you launched it (and subfolders)
- Create new files
- Edit existing files
- Run terminal commands (Python scripts, Git commands, package installs)
- Search your codebase
- Access the web (for documentation, package info)

### The Permission System

Claude Code asks permission before taking most actions. You control this through three tiers:

**Allow (runs without asking):** Safe, read-only, or routine commands
**Ask (requests approval each time):** Anything that modifies files or runs scripts
**Deny (blocked completely):** Dangerous commands you never want to run

### Your Starter Safety Configuration

Create this file at `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "bash:ls*",
      "bash:cat*",
      "bash:echo*",
      "bash:pwd",
      "bash:git status",
      "bash:git diff*",
      "bash:git log*",
      "bash:python --version",
      "bash:pip list"
    ],
    "deny": [
      "bash:rm -rf*",
      "bash:rm -r*",
      "bash:del*",
      "bash:curl*",
      "bash:wget*",
      "bash:ssh*",
      "read:.env*",
      "read:./secrets/**",
      "read:**/.ssh/**",
      "edit:.env*"
    ]
  }
}
```

### Critical Safety Rules

1. **File deletion bypasses trash.** When Claude Code deletes a file, it's gone forever. Never approve `rm` commands. Do deletions yourself through your file explorer.

2. **Always launch from a project folder.** Running `claude` from your home directory gives it read access to everything. Instead, always `cd` into a specific project first.

3. **Git is your undo button.** Commit working code frequently. If Claude Code breaks something, `git checkout .` restores your last commit.

4. **Read before approving.** Especially in the first weeks, read what Claude Code proposes before saying yes. This is also how you learn.

5. **Use Plan mode for learning.** Type `/plan` in Claude Code to make it plan before acting. This shows you its reasoning, which is itself educational.

6. **Use Sandbox mode for experiments.** Type `/sandbox` to enable filesystem and network isolation. Good for trying things you're unsure about.

7. **API keys and secrets go in `.env` files.** Never hardcode them. Add `.env` to both your `.gitignore` and Claude Code's deny list.

8. **The `--dangerously-skip-permissions` flag exists. Never use it.** It removes all safety checks. Some tutorials recommend it for speed. Ignore that advice until you're very experienced.

### CLAUDE.md — Project-Level Instructions

Each project folder should have a `CLAUDE.md` file that tells Claude Code about the project. Example for a learning project:

```markdown
# AI Learning Exercises

## About
Pablo's Python and AI learning exercises. Beginner level.

## Rules
- Explain every new concept before using it
- Add comments to all code
- Use simple, readable patterns over clever ones
- When I ask you to build something, show me the plan first
- Never delete files — only create or modify

## Structure
- /exercises/ — Python practice files
- /projects/ — Build projects
- /notes/ — Concept summaries
```

---

## Part 3: The Revised Roadmap — With Python Exercises

### How Each Week Works

```
DAY 1 (1.5-2h): PYTHON FUNDAMENTALS
  - Learn new Python concepts in Claude Chat (your Project)
  - Do structured exercises: write code BY HAND in VS Code
  - These are NOT project work — they're skill building
  
DAY 2 (1.5-2h): CONCEPT + DEMO
  - Learn the AI/tool concept for this week
  - See how it connects to the Python you just learned
  - Plan the week's mini-project

DAY 3 (1.5-2h): GUIDED BUILD
  - Open Claude Code in VS Code
  - Build the project together with Claude Code
  - You handle the parts you know; Claude Code handles the rest
  - Ask Claude Code to explain anything you don't understand

DAY 4 (1-1.5h): EXTEND + COMMIT
  - Add one feature YOURSELF (without Claude Code)
  - Debug any issues (with Claude Code as helper, not doer)
  - Commit to Git
  - Update your Progress Log and Session Handoff Block

WEEKEND (optional 2-3h): 
  - Review the week's Python concepts
  - Extend the project
  - Read one article or tutorial about the concept
```

---

### Phase 0: Setup & Orientation (Days 1-3)

**Day 1: Environment Setup**
- Create Claude Project "AI Builder — Learning" with instructions and docs (see Part 1)
- Create a folder structure on your computer:
  ```
  ~/ai-builder/
    /exercises/       ← Python practice files
    /projects/        ← Build projects (each gets its own subfolder)
    /notes/           ← Your own notes and summaries
  ```
- Open VS Code, open the `ai-builder` folder
- Install the Python extension in VS Code

**Day 2: Claude Code Orientation**
- Open terminal in VS Code, `cd ~/ai-builder`, run `claude`
- Do the three orientation sessions from the previous roadmap version:
  - Session 0.1: First Contact (create, run, and modify a script)
  - Session 0.2: Security Setup (configure settings.json, practice saying no)
  - Session 0.3: VS Code Integration (see files appear in real-time)

**Day 3: Git Foundations**
- In Claude Code: "Teach me Git basics. Initialize this folder as a Git repo, explain what each command does."
- Learn: `git init`, `git add`, `git commit`, `git status`, `git log`, `git diff`
- Create your GitHub account (you have one already — connect it)
- Push your first repo
- Understand: Git = save points. Commit every time something works.

**Checkpoint:** You can launch Claude Code, approve/decline actions, use VS Code, and commit code to Git. Your Claude Project is set up with the roadmap, progress log, and skills tracker uploaded.

---

### Phase 1: Python Foundations + First Tools (Weeks 1-3)

#### Week 1: Core Python — Variables, Data Structures, Functions

**Day 1 — Python Exercises (in Claude Chat Project):**

Topic: Variables, types, strings, f-strings

Exercises (write these yourself in VS Code, not Claude Code):
```
Exercise 1: Create variables for your name, age, and university. Print a sentence using f-strings.

Exercise 2: Write a script that converts temperature from Celsius to Fahrenheit and prints both.

Exercise 3: Given a full name string, extract the first name and last name using string methods.

Exercise 4: Create a script that takes a sentence and prints: the number of characters, the number of words, the sentence in uppercase, and the sentence reversed.
```

Topic: Lists and dictionaries

Exercises:
```
Exercise 5: Create a list of 5 cities you've lived in. Print the first, last, and middle one. Add a new city. Remove one.

Exercise 6: Create a dictionary representing a student (name, age, courses, grades). Print specific values. Add a new course. Update a grade.

Exercise 7: Given a list of numbers, create a new list containing only the even numbers. (Hint: use a for loop, then try list comprehension)

Exercise 8: Create a dictionary that maps course names to grades. Write code that calculates the average grade and finds the highest-graded course.
```

**Day 2 — Python Exercises continued:**

Topic: Functions, loops, conditionals

Exercises:
```
Exercise 9: Write a function called `greet(name, greeting="Hello")` that returns a greeting string. Call it with and without the greeting argument.

Exercise 10: Write a function that takes a list of numbers and returns a dictionary with keys "sum", "average", "min", and "max".

Exercise 11: Write a function that takes a string and returns a dictionary of character frequencies. Example: "hello" → {"h": 1, "e": 1, "l": 2, "o": 1}

Exercise 12: Write a function that takes a list of dictionaries (representing students with "name" and "grade" keys) and returns the names of students with grades above a given threshold.
```

**Day 3 — Python Exercises + First Mini-Project:**

Topic: File I/O and JSON

Exercises:
```
Exercise 13: Write a script that creates a text file, writes 5 lines to it, then reads it back and prints each line with a line number.

Exercise 14: Create a dictionary representing your weekly schedule. Save it as a JSON file. Then read it back and print Monday's activities.

Exercise 15: Write a function that reads a text file and returns a dictionary with: line_count, word_count, character_count, and most_common_word.
```

**Day 4 — Build: Text File Analyzer (with Claude Code)**

Now use Claude Code to build a more complete version:
> "I want to build a text analyzer tool. I've learned Python basics this week — variables, lists, dicts, functions, file I/O, and JSON. Help me build a script that: reads any text file, analyzes it (word count, sentence count, most common words, average word length, reading time estimate), and saves the results as a formatted JSON file. Show me your plan first."

**Day 5 — Extend + Commit:**
- Add a feature yourself: make it also analyze word length distribution
- Commit to Git with a clear message
- Update Progress Log

---

#### Week 2: Error Handling, APIs, and Environment Variables

**Day 1 — Python Exercises:**

Topic: Error handling (try/except), imports, pip

Exercises:
```
Exercise 16: Write a script that asks the user for two numbers and divides them. Handle: division by zero, non-numeric input. Print helpful error messages.

Exercise 17: Write a function that reads a JSON file. If the file doesn't exist, return an empty dictionary instead of crashing. If the JSON is malformed, print an error and return empty.

Exercise 18: Install the `requests` library using pip. Import it and print its version. Then install `python-dotenv` and print its version.

Exercise 19: Create a .env file with a variable MY_NAME="Pablo". Write a script that loads it and prints the value. Then add .env to .gitignore and explain why.
```

**Day 2 — Concept: APIs and HTTP:**

Learn in Claude Chat:
- What an API is (a way for programs to talk to each other)
- HTTP requests: GET (fetch data) vs. POST (send data)
- Headers, authentication, request body, response body
- Status codes: 200 (success), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)
- JSON as the language APIs speak

Exercises:
```
Exercise 20: Use the requests library to GET https://api.github.com. Print the status code and the JSON response.

Exercise 21: Write a function that takes a GitHub username and returns their public repo count. Handle the case where the username doesn't exist.

Exercise 22: Create a script that fetches a random quote from a free API (e.g., https://api.quotable.io/random), extracts the quote and author, and saves them to a JSON file. Add error handling for network failures.
```

**Day 3 — Concept: Calling Claude's API:**

Learn in Claude Chat:
- The Anthropic Python SDK
- System prompts vs. user messages in the API
- API keys and security
- Response parsing
- Token counting and costs

Exercise:
```
Exercise 23: Write a script that:
1. Loads your Anthropic API key from a .env file
2. Sends a simple message to Claude ("What is Python in one sentence?")
3. Prints the response
4. Handles potential errors (no API key, network failure, API error)
```

**Day 4 — Build: Document Summarizer (with Claude Code)**
> "Build a Python script that reads a text file, sends it to Claude's API with a system prompt designed for summarization, and saves the summary. Include error handling, environment variable management, and make the system prompt configurable."

**Day 5 — Extend + Commit:**
- Modify the system prompt yourself to produce different summary styles (bullet points vs. paragraph vs. executive summary)
- Add a feature: let the user choose summary length via a command-line argument
- Commit to Git

---

#### Week 3: Structured Outputs, Project Organization, and Building Reliably

**Day 1 — Python Exercises:**

Topic: Classes (basic), command-line arguments, project structure

Exercises:
```
Exercise 24: Create a simple class called Document with attributes: title, content, word_count. Add a method summarize() that returns the first 100 characters. Create two instances and print their summaries.

Exercise 25: Write a script that accepts command-line arguments using argparse: an input file path and an optional output file path. If no output path is given, print to screen.

Exercise 26: Refactor your text analyzer from Week 1 into a proper project structure:
  text_analyzer/
    main.py         (entry point)
    analyzer.py     (analysis functions)
    file_utils.py   (file reading/writing functions)
    config.py       (settings and defaults)
```

**Day 2 — Concept: Structured Outputs from LLMs:**

Learn in Claude Chat:
- What structured outputs are (getting JSON back from Claude, not just text)
- How to prompt for reliable JSON
- Response parsing and validation
- When structured outputs matter (any time code needs to process the response)

Exercises:
```
Exercise 27: Write a prompt that makes Claude return a JSON object with exactly these fields: {"summary": "...", "key_points": [...], "sentiment": "positive/negative/neutral", "word_count": N}. Parse the response in Python and print each field separately.

Exercise 28: Build a "structured extractor" — given a messy block of text about a person (name, job, location, interests), get Claude to return clean JSON. Handle cases where some fields might be missing.
```

**Day 3-4 — Build: Meeting Notes Processor (with Claude Code)**

Combined project that uses everything from Weeks 1-3:
> "Build a meeting notes processor. It should: read a transcript text file, send it to Claude with a system prompt that extracts decisions, action items, questions, and a summary as structured JSON, save the results, and handle errors gracefully. Use a proper project structure with separate modules."

**Day 5 — Extend + Commit:**
- Add a feature yourself: generate a follow-up email draft from the extracted action items
- Practice using Git branches: create a branch for the new feature, merge it when done
- Update Progress Log and Python Skills Tracker
- Upload updated trackers to your Claude Project

---

### Phase 2: Real Tools (Weeks 4-7)

#### Week 4-5: Daily Email + Calendar Briefing

**Python exercises first:**
```
Exercise 29: Write a script that works with dates and times — get today's date, format it, calculate days until a deadline, check if a time is in the morning/afternoon.

Exercise 30: Write a function that takes a list of dictionaries (representing emails with "from", "subject", "date", "body") and returns them sorted by date, with a "priority" field added based on keywords in the subject.

Exercise 31: Write a function that takes calendar events (list of dicts with "title", "start_time", "end_time", "attendees") and generates a text summary of the day.
```

**Then build with Claude Code:**
- Use MCP connectors (Gmail, Google Calendar) available in your Claude setup
- Start with sample/mock data, then connect real data sources
- Learn: prompt chaining, multi-step processing, configuration files

**New concepts:** MCP (Model Context Protocol), prompt chaining, scheduled workflows

#### Week 5-6: Personal Finance Analyzer

**Python exercises first:**
```
Exercise 32: Use Python's csv module to read a CSV file. Print the headers and first 5 rows.

Exercise 33: Given a list of transactions (dicts with "date", "description", "amount", "category"), write functions to: calculate total spending, spending per category, daily average, and top 5 largest transactions.

Exercise 34: Write a function that takes a list of uncategorized transactions and groups similar ones using simple string matching rules you define.
```

**Then build:** CSV ingestion → Claude categorization → spending summary report
**New concepts:** Working with tabular data, batch API calls, data validation

#### Week 6-7: Research Synthesis Assistant

**Python exercises first:**
```
Exercise 35: Write a function that splits a long text into chunks of roughly N words, with overlap between chunks.

Exercise 36: Write a function that takes multiple text summaries and generates a "synthesis" prompt — combining them into one coherent briefing.
```

**Then build:** Multi-document intake → per-document summary → cross-document synthesis → final memo
**New concepts:** Text chunking (pre-RAG skill), multi-document processing, template-based output

---

### Phase 3: Understanding the AI Stack (Weeks 8-11)

#### Week 8-9: RAG From Scratch

**Python exercises first:**
```
Exercise 37: Write a function that computes cosine similarity between two lists of numbers. Test it with simple examples to build intuition.

Exercise 38: Write a simple keyword-based search function: given a query and a list of text chunks, return the chunks that share the most words with the query.
```

**Build in stages:**
1. Manual RAG with keyword matching (no vector DB)
2. Add embeddings (understand what they are by using them)
3. Add ChromaDB as a simple vector store
4. Build Q&A bot over your MBA course materials

**Concepts:** Embeddings, vector search, chunking strategies, retrieval quality, citations

#### Week 10-11: The Decision Framework + Advanced Prompting

**The prompting vs. RAG vs. fine-tuning vs. LoRA framework** (see detailed section in previous roadmap version)

**Build:** A one-page consulting brief explaining when to use each approach
**Build:** An "AI Readiness Assessment" questionnaire for clients

---

### Phase 4: Building for Others (Weeks 12-16)

#### Week 12-13: Company Knowledge Assistant
- Multi-document RAG with metadata filtering
- PDF handling, confidence scoring
- This is your consulting demo project

#### Week 14-15: Workflow Automation Agent
- Tool calling and multi-step orchestration
- Human-in-the-loop design
- Error recovery patterns

#### Week 16: Deploy One Tool
- Streamlit for a simple web interface
- Railway or Render for hosting
- Secrets management, logging

---

### Phase 5: Consulting Toolkit + Foundations for Startup (Weeks 17-20)

- Polished decision framework one-pager
- AI Readiness Assessment template
- Scoping document template for AI projects
- Working demo customizable for different clients
- Architecture patterns for production AI systems

---

## Part 4: Artifacts and Interactive Learning

When we create interactive lessons, apps, or visualizations during our sessions, here's how they'll be preserved:

1. **Artifacts created in Claude Chat** — These render in the chat and can be revisited by scrolling back in the conversation. For important ones, I'll also provide the code so you can save it.

2. **Files created during sessions** — I can generate downloadable files (HTML apps, Python scripts, visualizations). Save these in your `~/ai-builder/notes/` folder.

3. **Key concept visualizations** — When I create diagrams or interactive explainers, save the link or screenshot to your Progress Log so you can find them later.

4. **Your Claude Project conversation history** — All conversations within a Project are saved and searchable. You can scroll back to any previous lesson.

The rule: **if something was useful, save it outside the chat** (as a file, a note, or a screenshot). Chat history is searchable but not perfectly reliable for long-term reference.

---

## Part 5: Expanded Use Case Library

### Personal Productivity
- Morning briefing agent (email + calendar + tasks + weather)
- Meeting prep assistant (pull context before any meeting)
- Research synthesis tool (summarize multiple papers into a memo)
- Personal CRM (track contacts, conversations, follow-ups)
- Reading prioritizer (summarize and rank your reading list)
- Travel planner with constraint optimization
- Expense categorizer and tax prep assistant
- Habit/goal tracker with weekly AI coaching summaries

### Small Business / Freelance Consulting
- Contract review assistant (flag risky clauses, suggest edits)
- Proposal generator from intake calls or notes
- Customer feedback analyzer (categorize themes from reviews/surveys)
- Onboarding workflow automator for new hires
- Invoice processor and reconciler
- SOP writer from process descriptions
- Client communication drafter (status updates, deliverable summaries)

### Enterprise / McKinsey-Tier
- Compliance monitoring agent (regulatory change alerts)
- RFP response drafter from historical proposals
- Board report generator from multiple data sources
- Internal knowledge search across departments
- Supply chain disruption alerter with news monitoring
- Competitive intelligence workflow (automated monitoring + synthesis)
- Policy document navigator for large organizations
- M&A due diligence document analyzer
- Change management communication drafter

### Energy Sector Specific
- Permit and regulatory document navigator
- Equipment maintenance predictor (from logs + manuals)
- ESG reporting automator
- Safety incident report analyzer and trend detector
- Field operations Q&A bot (technician reference tool)
- Energy market daily briefing (prices, regulation, news)
- Grid operations anomaly detector
- Environmental compliance checker

### Advanced (Post-Roadmap)
- Multi-agent research team (search → analyze → write)
- Data analyst agent (connect databases, run queries, generate charts)
- Recruitment screening assistant
- Sales call prep agent (CRM + news + relationship history)
- Lead qualification agent
- Code review assistant
- Documentation generator from codebases

---

## Part 6: Concepts Reference

### Glossary for Beginners

**API (Application Programming Interface):** A way for programs to talk to each other. When you call Claude's API, your Python script sends a request and gets a response back.

**Embeddings:** Numerical representations of text. Similar texts get similar numbers. Used for search and RAG.

**RAG (Retrieval-Augmented Generation):** A technique where you first search for relevant documents, then send them to an AI along with a question. This lets AI answer questions about specific data it wasn't trained on.

**Fine-tuning:** Retraining an existing AI model on your specific data to change its behavior. Expensive and usually unnecessary — prompting + RAG handles most cases.

**LoRA (Low-Rank Adaptation):** A cheaper way to fine-tune open-source models by only updating a small portion of the model's parameters.

**MCP (Model Context Protocol):** How Claude connects to external services like Gmail, Google Calendar, Slack. It handles authentication and data retrieval.

**System Prompt:** Instructions given to an AI that set its role, constraints, and behavior. In the API, it's a separate parameter from the user message.

**Context Window:** The maximum amount of text an AI can process at once. Claude's is ~200,000 tokens (~150,000 words). This is why RAG exists — most knowledge bases are too large to fit in one prompt.

**Token:** The basic unit AI models process. Roughly ¾ of a word. Longer prompts = more tokens = higher cost.

**Vector Database:** A specialized database for storing and searching embeddings. Examples: ChromaDB (local), Pinecone (cloud).

**Tool Calling / Function Calling:** When an AI decides which tools to use based on a request. Example: Claude deciding to search your email vs. check your calendar based on what you asked.

**Prompt Chaining:** Breaking a complex task into steps where the output of one prompt becomes the input to the next.

**Structured Output:** Getting an AI to return data in a specific format (usually JSON) that code can parse reliably.

**Git:** A version control system that tracks changes to your code. Think of it as unlimited undo with save points.

**GitHub:** A website that hosts Git repositories online. Backup + portfolio + collaboration.

---

## Immediate Next Steps

1. Create your Claude Project "AI Builder — Learning"
2. Upload this roadmap and the Progress Log template to it
3. Set the custom instructions (provided in Part 1)
4. Create the folder structure on your computer
5. Start Phase 0, Day 1

When you're ready, come back to this Project and say: "I've completed the setup. Ready for Phase 0, Day 2 — Claude Code orientation."
