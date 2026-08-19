"""Browser & Actions Sub-Agent: Interacts with the browser and manages open tabs."""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

try:
    from tools.browser_tools import (
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
    )
except ImportError:
    from ..tools.browser_tools import (
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
    )

browser_agent = Agent(
    name="browser_operator",
    model=DEFAULT_MODEL,
    description=(
        "Specialist in real-time browser automation, tab listing, and navigation. "
        "Use this agent whenever the user asks: "
        "1. How many tabs are open or what tabs/websites are active. "
        "2. To open YouTube or search inside an existing YouTube tab without opening duplicate tabs. "
        "3. To open or switch to specific websites (Gmail, GitHub, etc.). "
        "4. To close a specific browser tab."
    ),
    instruction=(
        "You are an expert Tab-Aware Browser Automation Assistant.\n\n"
        "### MANDATORY ACTION INSTRUCTIONS:\n"
        "1. **Tab Listing:** When asked what tabs are open, how many tabs exist, or to inspect active pages, YOU MUST CALL `list_open_browser_tabs`. NEVER claim lack of visibility.\n"
        "2. **Smart YouTube Searches (Prevent Duplicates):** When the user asks to open YouTube or search within YouTube, call `search_youtube`. It automatically reuses existing tabs.\n"
        "3. **Smart Navigation (Prevent Duplicates):** When opening any URL or web app (e.g. Gmail, GitHub), call `open_or_reuse_tab`.\n"
        "4. **Close Tabs:** Call `close_browser_tab` when requested.\n"
        "5. **Response:** Format tab lists with markdown bullet points showing the Tab Name and Link."
    ),
    tools=[
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
    ],
)
