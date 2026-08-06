# Stonxs — Stock Sentiment AI Agent

A Streamlit application that runs a small set of agent-like functions to fetch a stock's price, gather recent news, and produce a short sentiment read plus a more detailed sentiment/filings-based forecast for a single ticker symbol.

## Features

- Get the latest price for a ticker using yfinance (backend/tools.py)
- Fetch recent stock news from yfinance and Google News (backend/tools.py)
- Run a multi-source sentiment forecast that consults price, news, web search, quarterly financials, and EDGAR filings (backend/stock_agents.py)
- Basic input filtering: simple pattern checks and an LLM-based safety check to block non-ticker inputs (backend/security.py)
- Streamlit UI that lets you choose an LLM provider (local Ollama URL or a custom cloud endpoint) and the model name (frontend/frontend.py)

## Tech Stack

- Python
- Streamlit (UI)
- yfinance (market data)
- ddgs (DuckDuckGo search helper)
- gnews (Google News wrapper)
- edgartools (EDGAR access)
- openai-agents (agent and Runner abstractions used by the backend)

Dependency list is in `requirements.txt` at the repository root.

## Prerequisites

- Python (create a virtual environment before running)
- Git (to clone the repo)

Note: `requirements.txt` pins Streamlit and other libraries; follow the Installation steps below.

## Installation

Run these commands in Git Bash from the repository root:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

`requirements.txt` exists at the project root and is used by `setup_check.py` and by the installation step above.

## Usage

Start the Streamlit app from Git Bash:

```bash
python -m streamlit run app.py
```

When the app runs it opens a Streamlit UI in the browser. The first screen shows the page title and a sidebar with LLM provider settings. Enter a ticker (for example `TSLA`) and submit to run the backend agents.

`app.py` calls `setup_check.run_all_checks()` on startup; that helper will create a `.venv` and attempt to install requirements if they are missing.

## Project structure

Only the files and folders that matter for running and extending the app are listed below.

- `app.py` — entry point. Sets up module paths, runs startup checks, and launches the Streamlit frontend.
- `frontend/frontend.py` — Streamlit UI, provider settings, input validation, and orchestration of agent runs.
- `backend/tools.py` — functions that fetch data: stock price, analyst recommendations, news, web search, quarterly financials, and EDGAR filings.
- `backend/stock_agents.py` — agent definitions and instructions that drive which tools get called and how results are formatted.
- `backend/security.py` — contains `check_message_basic` (pattern checks) and `check_message_with_ai` (calls an Agent via Runner to validate input).
- `setup_check.py` — helper that creates a `.venv`, installs `requirements.txt`, and asserts required files exist.
- `requirements.txt` — dependency list used by the project.

There is a `.venv` directory in the repository root (if you cloned or the project was run locally). The code expects the backend and frontend packages to be importable from the project root (see `sys.path` manipulation in `app.py`).

## Configuration

The Streamlit UI writes two environment variables before running agent calls. You can also set these in your shell if you prefer.

- `OPENAI_BASE_URL` — Base URL for the LLM provider. The UI defaults to `http://localhost:11434/v1` for "Ollama (local)" and `https://api.openai.com/v1` when "Custom / Cloud" is chosen (see `frontend/frontend.py`).
- `OPENAI_API_KEY` — API key or token for the provider. The code sets this to the provided API key or to the literal string `ollama` when left empty.

Model name defaults visible in the UI:

- Local default model: `gemma4:31b-cloud`
- Cloud default model shown in the UI: `gpt-4o-mini`

Those defaults are set in `frontend/frontend.py` and then written into the corresponding agent objects at runtime.

## Running tests

This repository does not include a test suite or a `tests/` folder.

## Contributing

If you make changes, run the app locally to verify behaviour. Keep changes focused and include a short description of how you tested the change in your pull request.

## License

This project is licensed under the MIT License. See `LICENSE` in the repository root.


---

Summary of sources and assumptions

- Features and behaviour: taken from `frontend/frontend.py`, `backend/tools.py`, `backend/stock_agents.py`, and `backend/security.py` (the code paths show what the app actually calls and how it validates input).
- Entry point and startup behaviour: `app.py` calls `setup_check.run_all_checks()` and then `frontend.run_app()`; `setup_check.py` shows venv creation and requirements installation.
- Dependencies: read from `requirements.txt`.
- Configuration environment variables and defaults: read from `frontend/frontend.py` (OPENAI_BASE_URL, OPENAI_API_KEY, and the UI defaults for model names).

Assumptions made

- Python version requirement is not explicitly stated in the repository; the README does not pin an exact Python version. The installer commands use the provided `requirements.txt`.
- No test framework was found; therefore there is no "Running tests" section beyond noting its absence.

If you want a different project title line or a shorter/longer summary for contributors, tell me and I will update the README accordingly.
