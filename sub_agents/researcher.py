"""Researcher Sub-Agent: Gathers information and investigates topics."""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

try:
    from tools.search_tools import search_knowledge_base, fetch_webpage_content
except ImportError:
    from ..tools.search_tools import search_knowledge_base, fetch_webpage_content

researcher_agent = Agent(
    name="researcher",
    model=DEFAULT_MODEL,
    description=(
        "Specialist in researching topics, retrieving technical facts, "
        "and fetching webpage content from URLs. Delegate here when you need information gathered or web links analyzed."
    ),
    instruction=(
        "You are an expert Research Analyst. Your job is to:\n"
        "1. Understand the user's research objective or topic query.\n"
        "2. Use `search_knowledge_base` to find facts or `fetch_webpage_content` to read links from user tabs/articles.\n"
        "3. Structure your findings into clear bullet points, noting key insights and trade-offs.\n"
        "4. Return clear, objective, and well-organized research notes."
    ),
    tools=[search_knowledge_base, fetch_webpage_content],
)
