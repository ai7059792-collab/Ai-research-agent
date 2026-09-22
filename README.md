# 🔎 AI Research Agent

A beginner-friendly single-agent AI research application built with:

- CrewAI
- Groq
- `openai/gpt-oss-120b`
- DuckDuckGo search (`ddgs`)
- Streamlit

## Project Structure

```text
ai-research-agent/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Deployment

This project is designed to be uploaded directly to GitHub and deployed on Streamlit Community Cloud.

No local setup is required.

### 1. Upload to GitHub

Upload these files to your GitHub repository:

- `app.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

### 2. Deploy on Streamlit Community Cloud

Create a new Streamlit app from your GitHub repository.

Set the main file to:

```text
app.py
```

### 3. Add the Groq API Key

In your Streamlit app:

**Settings → Secrets**

Add:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

The application reads the API key from Streamlit Secrets only.

Do not put your API key inside `app.py` or upload it to GitHub.

## How the Agent Works

```text
User enters research topic
          ↓
     Streamlit UI
          ↓
     CrewAI Agent
          ↓
 DuckDuckGo Web Search
          ↓
     Groq LLM
          ↓
    Research Report
```

The application uses one CrewAI agent. The agent searches the web, analyzes the gathered information, and produces a structured research report.
