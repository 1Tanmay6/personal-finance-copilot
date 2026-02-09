# Personal Finance Agent

**Privacy-first, 100% local personal finance assistant** powered by Ollama and LangGraph.  
Runs entirely offline on your computer **no cloud, no telemetry, no data ever leaves your device**.

### What it does (Phase 1 MVP)

- Import transactions from CSV or manual entry
- Automatically categorize spending (optimized for Indian UPI, Swiggy, Paytm, Amazon-style descriptions)
- Show spending summaries, category breakdowns, month-to-month changes
- Detect spending leaks and generate simple alerts
- Track progress toward your emergency fund goal
- Answer natural language questions about your finances

All processing and reasoning happens locally using Ollama (default non-thinker: Qwen 2.5 coder & thinker: Qwen 3).

### Architecture Overview (Phase 1)

![alt text](<Personal Finance Co-pilot.jpg>)

- **Chat Agent**: Handles user conversation, routes queries, formats responses
- **Analysis Agent**: Computes metrics, detects patterns, runs background scans
- **Data Service**: Central utility for import, parsing, querying, storage (no LLM)
- **Local SQLite**: Single file `finance.db` - transactions, goals, settings

All agents use narrow, predefined tools - no dangerous capabilities.

### Tech Stack (Phase 1)

- Python 3.10+
- LangGraph - agent orchestration & graph workflows
- Ollama + Llama 3.1 (local LLM)
- SQLite - local database
- Streamlit - UI (chat + dashboard)
- pandas - data manipulation
- asyncio - async-first design

### Privacy & Security

- 100% local execution - no internet required (except optional cloud LLM)
- No telemetry, no analytics, no external APIs by default
- Data stored in a single local file (`~/.personal-finance-agent/finance.db`)
- Open-source - you can audit everything
- Agents only access data through whitelisted, narrow tools

### Quick Start (to be filled soon)

```bash
# 1. Clone the repo
git clone https://github.com/1Tanmay6/personal-finance-copilot.git
cd personal-finance-copilot

# 2. Install dependencies
uv sync

# 3. Install & run Ollama (one-time)
# Download from https://ollama.com
ollama run llama3.1

# 4. Run the app
streamlit run app/ui/app.py
```

### Project Status

    Phase 1 MVP in progress — focused on spending control + emergency fund tracking.

### License

    MIT License — free to use, modify, distribute.

### Author

    Tanmay — Bengaluru
    Finance Tacker for agentic AI, system design, and async Python skills.
