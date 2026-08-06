Stock Sentiment AI Agent

A small Streamlit application that runs a set of AI "agents" to fetch stock prices, surface recent news, and produce a short sentiment read plus a more detailed sentiment/filings-based forecast. The app exists to provide evidence-based, tool-sourced signals for a single ticker symbol (no trading or portfolio management features).

Features

- Lookup the current stock price for a ticker using yfinance
- Pull recent stock-related news and surface short sentiment bullets
- Run a detailed sentiment forecast that consults price, news, web search, quarterly financials, and SEC (EDGAR) filings
- Basic input security checks (simple pattern checks and an AI-based filter) to block non-ticker inputs
- Streamlit UI with configurable LLM provider settings (local Ollama or a custom cloud endpoint)

Tech stack / built with

- Python
- Streamlit (UI)
- yfinance (market data)
- ddgs (DuckDuckGo search helper)
- gnews (Google News wrapper)
- edgartools (EDGAR access)
- openai-agents (agent/Runner abstractions used by the project)
- Additional libraries listed in <./requirements.txt> (see link below)

Prerequisites

- Python 3.8 or later (a virtual environment is recommended)
- Git (to clone the repository)
- Network access (the app makes web/API calls for market data, news, and LLM providers)

Installation

Open Git Bash and run the following commands from the repository root.

1. Create a virtual environment: python -m venv .venv
2. Activate it in Git Bash: source .venv/Scripts/activate
3. Install dependencies: pip install -r requirements.txt

Adjust the requirements file name above only if your repository uses a different file; this repository provides <requirements.txt> at the project root.

Configuration

- The Streamlit UI exposes LLM provider settings in the sidebar. Those settings map to the environment variables the code uses at runtime:
  - OPENAI_BASE_URL: base URL for the LLM provider (default values are provided in the UI)
  - OPENAI_API_KEY: API key or token for the provider (the UI stores it in an environment variable before launching calls)

- The frontend code defaults to a local Ollama-like URL (http://localhost:11434/v1) when "Ollama (local)" is chosen in the sidebar and otherwise uses the provided base URL and API key.

- There is a small startup helper <setup_check.py> that will create a .venv and install requirements when run; the app's main entrypoint calls it at startup.

Usage

Run the Streamlit app from Git Bash with:

```bash
python -m streamlit run app.py
```

This opens the Streamlit app in your browser.

Project structure

- <app.py> — project entry point; runs startup checks and launches the Streamlit frontend
- <frontend/frontend.py> — Streamlit UI and orchestration (page layout, settings, running agents)
- <backend/> — backend agent definitions and helper tools
  - <backend/tools.py> — tool functions used by agents (yfinance, web searches, EDGAR access)
  - <backend/stock_agents.py> — agent definitions and instructions
  - <backend/security.py> — basic and AI-based input filtering
- <requirements.txt> — Python dependencies used by the project
- <setup_check.py> — creates a venv, installs requirements, and validates required files on startup

Contributing

- If you plan to contribute, ensure the repository runs locally:
  - Create and activate a virtual environment and install requirements (see Installation)
  - Run <app.py> or run the Streamlit command above to exercise the app
- Open a focused pull request with a clear description of the change and a small, self-contained diff
- If adding or changing dependencies, include a note explaining why and verify the app still starts

License

This project is offered under the MIT License. See the <LICENSE> file in the repository root for the full text.

References and notes

- Entry point: <app.py> (the file that calls into <frontend/frontend.py>)
- Requirements file found at: <requirements.txt>
- Startup checks and venv creation are implemented in <setup_check.py>

