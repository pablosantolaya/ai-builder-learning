# AI Builder — Learning Project

## Critical Rules
- Always use encoding="utf-8" in open() calls (Windows cp1252 breaks special characters)
- Use __file__ + os.path.dirname(__file__) to anchor file paths to script location
- Never delete files — only create or modify
- Real financial data stays local — always in .gitignore
- Always confirm before pushing to GitHub

## Tech Stack
- Python 3 on Windows (PowerShell terminal)
- VS Code with Python extension
- Git + GitHub (repo: pablosantolaya/ai-builder-learning)
- Anthropic SDK for Claude API calls
- API key stored in .env (never commit .env files)

## Project Structure
- exercises/          — Python practice files (day1_strings.py, etc.)
- projects/           — Build projects, each in its own subfolder
- projects/*/output/  — Generated output files (gitignored)
- notes/              — Concept summaries and progress logs

## How to Run
- Run scripts from inside their project folder: cd projects/finance_analyzer/
- Python command: python main.py

## Working With Me
- Explain every new concept before using it
- Add comments to all code
- Use simple, readable patterns over clever ones
- Show me the plan before building anything