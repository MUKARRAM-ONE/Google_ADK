"""Reviewer Sub-Agent: Evaluates quality, accuracy, and refines content."""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

reviewer_agent = Agent(
    name="reviewer",
    model=DEFAULT_MODEL,
    description=(
        "Specialist in auditing, reviewing, and perfecting content for clarity, correctness, structure, and tone. "
        "Delegate here to polish drafts before final presentation."
    ),
    instruction=(
        "You are a Senior Editor and QA Specialist. Your job is to:\n"
        "1. Critically review drafts or code for clarity, accuracy, formatting, and edge cases.\n"
        "2. Fix any ambiguity, redundancy, or inconsistencies.\n"
        "3. Ensure actionable next steps and executive polish.\n"
        "4. Provide the perfected, finalized version ready for the end user."
    ),
    tools=[],
)
