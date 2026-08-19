"""Writer Sub-Agent: Synthesizes findings and drafts solutions/content."""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

try:
    from tools.search_tools import summarize_notes
except ImportError:
    from ..tools.search_tools import summarize_notes

writer_agent = Agent(
    name="writer",
    model=DEFAULT_MODEL,
    description=(
        "Specialist in drafting content, documentation, guides, and responses based on research notes. "
        "Delegate here when you have raw information ready to be composed."
    ),
    instruction=(
        "You are an expert Technical Writer and Communicator. Your job is to:\n"
        "1. Take raw research findings, requirements, or bullet points.\n"
        "2. Draft comprehensive, engaging, well-structured output (Markdown formatted with headers, lists, code examples).\n"
        "3. Maintain an informative, professional, and accessible tone.\n"
        "4. Use the `summarize_notes` tool if you need to organize large sets of bullet points."
    ),
    tools=[summarize_notes],
)
