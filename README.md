# AI Research Agent - Fixed Version

This is a single-agent research application built with CrewAI, Groq, DuckDuckGo search, and Streamlit.

## Important fix

CrewAI routes the `groq/...` model through LiteLLM. The previous version installed `crewai` without the LiteLLM extra, which caused an ImportError when `LLM(...)` was created.

This version uses:

```text
crewai[litellm]==1.15.22
```

and the model:

```text
groq/openai/gpt-oss-120b
```

The Groq API key is read only from Streamlit Secrets.

## GitHub files

```text
ai-research-agent/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Streamlit Secrets

In Streamlit Cloud, open:

**App → Settings → Secrets**

Add:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

Do not upload your API key to GitHub.

## Deployment

1. Replace the old files in your GitHub repository with these files.
2. Commit the changes.
3. Streamlit Cloud will rebuild the application.
4. If needed, use **Manage app → Reboot app** after the dependency installation completes.
