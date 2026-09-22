import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from ddgs import DDGS

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Research Agent")
st.write(
    "Enter a research topic and let the AI Research Agent "
    "search the web and create a research report."
)

# ---------------------------------------------------------
# GROQ API KEY FROM STREAMLIT SECRETS ONLY
# ---------------------------------------------------------

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is not configured in Streamlit Secrets."
    )
    st.stop()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# CrewAI/LiteLLM expects the Groq provider key in this environment variable.
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# ---------------------------------------------------------
# DUCKDUCKGO SEARCH TOOL
# ---------------------------------------------------------

@tool("DuckDuckGo Web Search")
def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    try:
        results = DDGS().text(query, max_results=5)

        if not results:
            return "No search results were found."

        formatted_results = []

        for result in results:
            formatted_results.append(
                f"Title: {result.get('title', 'No title')}\n"
                f"Description: {result.get('body', 'No description')}\n"
                f"URL: {result.get('href', 'No URL')}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search error: {str(e)}"

# ---------------------------------------------------------
# GROQ LLM
# ---------------------------------------------------------

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0.2
)

# ---------------------------------------------------------
# SINGLE RESEARCH AGENT
# ---------------------------------------------------------

research_agent = Agent(
    role="AI Researcher",
    goal=(
        "Research the given topic using reliable web sources "
        "and create a clear, accurate and well-structured "
        "research report."
    ),
    backstory=(
        "You are an experienced research analyst. You carefully "
        "search for relevant information, compare sources, identify "
        "important facts, and organize findings into an easy-to-read "
        "report. Do not invent facts. When information is uncertain, "
        "clearly state the uncertainty."
    ),
    tools=[duckduckgo_search],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

research_topic = st.text_area(
    "Enter your research topic",
    placeholder="Example: Impact of artificial intelligence on manufacturing",
    height=120
)

report_length = st.selectbox(
    "Select report length",
    ["Short", "Medium", "Detailed"]
)

# ---------------------------------------------------------
# GENERATE REPORT
# ---------------------------------------------------------

if st.button("🚀 Generate Research Report", type="primary"):

    if not research_topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    if report_length == "Short":
        length_instruction = "Write approximately 500-700 words."
    elif report_length == "Medium":
        length_instruction = "Write approximately 900-1200 words."
    else:
        length_instruction = "Write approximately 1500-2000 words."

    research_task = Task(
        description=f"""
        Conduct research on the following topic:

        {research_topic}

        Instructions:
        1. Search the web using the DuckDuckGo search tool.
        2. Search for multiple relevant sources.
        3. Focus on reliable and useful information.
        4. Do not invent facts.
        5. Compare information when appropriate.
        6. Identify important facts, findings and trends.
        7. Include source URLs in the report.
        8. Organize the report using clear headings.
        9. Use simple and professional language.

        Report length:
        {length_instruction}

        The final report should contain:
        - Title
        - Introduction
        - Main findings
        - Detailed analysis
        - Important facts or statistics
        - Conclusion
        - Sources

        Research topic:
        {research_topic}
        """,
        expected_output="""
        A well-structured research report containing:
        1. Title
        2. Introduction
        3. Main findings
        4. Detailed analysis
        5. Important facts or statistics
        6. Conclusion
        7. Source URLs

        The report should be factual, clear and easy to understand.
        """,
        agent=research_agent
    )

    research_crew = Crew(
        agents=[research_agent],
        tasks=[research_task],
        verbose=True
    )

    with st.spinner(
        "🔎 Researching the topic and preparing your report..."
    ):
        try:
            result = research_crew.kickoff()

            st.success("Research completed!")
            st.markdown("---")
            st.subheader("📄 Research Report")
            st.markdown(str(result))

            st.download_button(
                label="📥 Download Report",
                data=str(result),
                file_name="research_report.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("Something went wrong while generating the report.")
            st.exception(e)
