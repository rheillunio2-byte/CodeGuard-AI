# CodeGuard AI

CodeGuard AI is a Python code-review dashboard combining local static analysis with streamed AI explanations from Google Gemini.

## Features

- Paste Python source code or upload a `.py` file
- Detect selected risky patterns with built-in CodeGuard rules
- Run Bandit security checks and Ruff quality checks
- Stream Gemini review output into the dashboard as it is generated
- Filter findings by severity and source
- Export filtered findings as CSV
- Dark cybersecurity-inspired interface

## Requirements

- Python 3.13 recommended
- A Gemini API key for AI reviews

## Setup on Windows

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `GEMINI_API_KEY` to your own key. Never commit `.env` to GitHub.

## Run

```powershell
python -m streamlit run app.py
```

## Run tests

```powershell
python -m unittest discover -s tests
```

## Notes

Static scans run locally. AI reviews send submitted code to Google Gemini. Remove API keys, passwords, tokens, and proprietary content before requesting a review unless you are authorized to share it. The tool does not execute submitted code and cannot guarantee that code is secure.
