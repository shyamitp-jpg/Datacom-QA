# Datacom QA - Bugs Form Automation

This repo contains automated UI tests for the Bug Report Form at:
https://qa-practice.netlify.app/bugs-form

## Tech Stack
- Python 3.11+
- Playwright (suggested framework)
- Behave (BDD)

## How to Run

```bash
# 1. Setup
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install playwright behave
playwright install

# 2. Run tests (headed + slow so you can watch)
behave --no-capture            # Shows print statements
# Or with color + stop on first failure
behave --stop -k