# QA Bugs Form Automation – Playwright + Pytest

This project automates UI validation for the Bug Form page:
https://qa-practice.netlify.app/bugs-form

## Framework
- **Language:** Python
- **Framework:** Pytest + Playwright
- **Pattern:** Page Object Model + Arrange–Act–Assert
- **Extras:** Screenshots on failure (auto)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
