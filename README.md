# 🔍 Canadian Trade Anomaly Detector

An AI-powered Streamlit application that detects anomalies in Canadian international trade data spanning 1990–2026, and uses an intelligent agent to automatically research and explain the cause of each anomaly in real time.

## 📌 Overview

This project combines statistical anomaly detection with a live AI agent to not only flag unusual spikes and drops in trade data, but explain *why* they happened — pulling real-time information from the web to provide context and answers.

## ✨ Features

- **Anomaly Detection** — Automatically flags abnormal spikes and drops in trade volume across the 1990–2026 timeframe
- **AI Agent** — An intelligent agent powered by Claude Sonnet searches the internet in real time to find and explain the cause of each flagged anomaly
- **Interactive UI** — Built with Streamlit for a clean, easy-to-use interface
- **Web Search** — Powered by Tavily API for live, accurate web search results

## 🏗️ How It Works

```
Trade Data (1990–2026)
        ↓
Anomaly Detection Algorithm
        ↓
Flagged Anomalies (spikes & drops)
        ↓
AI Agent (Claude Sonnet + Tavily Search)
        ↓
Real-time Explanation of Each Anomaly
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core application language |
| Streamlit | Web application framework |
| Claude Sonnet (Anthropic) | AI agent and reasoning |
| Tavily API | Real-time web search |
| Pandas | Data manipulation |
| Matplotlib / Plotly | Visualizations |

## 🚀 Running Locally

```bash
# Clone the repository
git clone https://github.com/frz08/trade-anomaly-detector

# Install dependencies
pip install -r requirements.txt

# Add your API keys to a .env file
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
trade-anomaly-detector/
│
├── app.py                  # Main Streamlit application
├── anomaly_detection.py    # Detection logic
├── agent.py                # AI agent configuration
├── data/                   # Trade datasets
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variable template
```


## 📬 Demo

This app runs locally. For a live demo, feel free to reach out — demo available on request.

---

*Developed by Farhaz Kolathoor*
