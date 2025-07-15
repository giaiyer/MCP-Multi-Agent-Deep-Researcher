import os
from dotenv import load_dotenv
import requests
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import re

# Load environment variables (for non-LinkUp settings)
load_dotenv()

def get_llm_client():
    return "ollama/phi3:latest"

class LinkUpSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="LinkUp Search",
            description="Search the web for information using LinkUp and return comprehensive results"
        )

    def _run(self, query: str, depth: str = "deep", output_type: str = "sourcedAnswer") -> str:
        api_key = os.getenv("LINKUP_API_KEY")
        url = "https://api.linkup.so/v1/search"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "depth": depth,
            "outputType": output_type
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return str(data.get("answer", data))
        except Exception as e:
            return f"Error occurred while searching: {str(e)}"

def clean_mcp_output(raw_text):
    # Remove "**Thought**" and "**Final Answer**" lines
    cleaned = re.sub(r"\*\*Thought\*\*.*\n?", "", raw_text)
    cleaned = re.sub(r"\*\*Final Answer\*\*.*\n?", "", cleaned)
    # Convert markdown headers to plain text with spacing
    cleaned = re.sub(r"^# (.*)", r"\n\1\n" + "="*40, cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^## (.*)", r"\n\1\n" + "-"*30, cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^### (.*)", r"\n\1\n" + "-"*20, cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^#### (.*)", r"\n\1\n" + "-"*10, cleaned, flags=re.MULTILINE)
    # Remove markdown bold/italics
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
    # Add spacing before References
    cleaned = re.sub(r"\n---\nReferences:", r"\n\nReferences:\n", cleaned)
    # Remove footnote markers like [^1], [^2]
    cleaned = re.sub(r"\[\^(\d+)\]", "", cleaned)
    # Remove extra blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()

def create_research_crew(query: str):
    llm_config = get_llm_client()
    linkup_search_tool = LinkUpSearchTool()

    web_searcher = Agent(
        role="Web Searcher",
        goal="Find the most relevant, comprehensive, and up-to-date information on the web. Gather a wide range of perspectives and details, but do not include source links or URLs in the final output.",
        backstory="An expert at formulating search queries and retrieving the most thorough, relevant information. Passes the results to the 'Research Analyst' only.",
        verbose=True,
        allow_delegation=True,
        tools=[linkup_search_tool],
        llm=llm_config,
    )

    research_analyst = Agent(
        role="Research Analyst",
        goal="Analyze and synthesize all raw information into a long, detailed, and clear report. Do not include sources, citations, or URLs. Do not include agent thoughts or process steps. Extract key insights, provide context, and ensure depth and accuracy.",
        backstory="An expert at analyzing information, identifying patterns, and extracting key insights. If required, can delegate the task of fact checking/verification to 'Web Searcher' only. Passes the final, in-depth analysis to the 'Technical Writer' only.",
        verbose=True,
        allow_delegation=True,
        llm=llm_config,
    )

    technical_writer = Agent(
        role="Technical Writer",
        goal="Create a long, well-structured, clear, and comprehensive response in markdown format. Do not include sources, citations, URLs, or any agent thoughts or process steps. The answer should be suitable for publication or expert review.",
        backstory="An expert at communicating complex information in an accessible, detailed, and authoritative way.",
        verbose=True,
        allow_delegation=False,
        llm=llm_config,
    )

    search_task = Task(
        description=f"Search for the most comprehensive, detailed, and up-to-date information about: {query}. Gather as many sources and perspectives as possible, but do not include source links or URLs in the final output.",
        agent=web_searcher,
        expected_output="Extensive, detailed raw search results including a wide range of perspectives, but no source links or URLs.",
        tools=[linkup_search_tool]
    )

    analysis_task = Task(
        description="Analyze the raw search results, identify all key information, verify facts, and prepare a long, structured, and in-depth analysis. Do not include sources, citations, URLs, or any agent thoughts or process steps. Provide context and synthesis only.",
        agent=research_analyst,
        expected_output="A long, structured, and in-depth analysis of the information with verified facts and key insights, but no sources, citations, or URLs.",
        context=[search_task]
    )

    writing_task = Task(
        description="Create a comprehensive, well-organized, and detailed response based on the research analysis. The answer should be long, clear, and directly answer the query, with no sources, citations, URLs, or agent thoughts/process steps in the output.",
        agent=technical_writer,
        expected_output="A long, clear, and comprehensive response that directly answers the query, with no sources, citations, URLs, or agent thoughts/process steps.",
        context=[analysis_task]
    )

    crew = Crew(
        agents=[web_searcher, research_analyst, technical_writer],
        tasks=[search_task, analysis_task, writing_task],
        verbose=True,
        process=Process.sequential
    )
    return crew

def run_research(query: str):
    try:
        crew = create_research_crew(query)
        result = crew.kickoff()
        return clean_mcp_output(result.raw)
    except Exception as e:
        return f"Error: {str(e)}" 