"""Root Coordinator Agent: Coordinates specialized sub-agents and provides interactive assistance."""
import sys
from pathlib import Path

# Ensure project root is in sys.path for ADK nested loader
_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

try:
    from sub_agents.researcher import researcher_agent
    from sub_agents.writer import writer_agent
    from sub_agents.reviewer import reviewer_agent
    from sub_agents.browser_agent import browser_agent
    from sub_agents.document_agent import document_agent
    from tools.browser_tools import (
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
    )
    from tools.ocr_tools import extract_text_from_image
except ImportError:
    from .sub_agents.researcher import researcher_agent
    from .sub_agents.writer import writer_agent
    from .sub_agents.reviewer import reviewer_agent
    from .sub_agents.browser_agent import browser_agent
    from .sub_agents.document_agent import document_agent
    from .tools.browser_tools import (
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
    )
    from .tools.ocr_tools import extract_text_from_image

# Root Interactive Coordinator Agent
root_agent = Agent(
    name="coordinator_assistant",
    model=DEFAULT_MODEL,
    description="Primary interactive coordinator assistant that introduces its capabilities and delegates to specialized sub-agents.",
    instruction=(
        "You are an intelligent, friendly Interactive Assistant and Multi-Agent Coordinator.\n\n"
        "### Persona & Greetings:\n"
        "- When the user greets you (e.g. 'hi', 'hello', 'hey') or asks about your capabilities, greet them warmly: "
        "'Hey! How are you today? I am your AI Multi-Agent Coordinator. Here are the key fields and areas I can help you with:'\n"
        "  1. 🖼️ **Document & Image Analysis:** Reading text, schedules, receipts, and tables directly from uploaded images or local files.\n"
        "  2. 🌐 **Live Browser & Tab Management:** Listing all active browser tabs, switching/reusing open tabs without opening duplicates, launching YouTube searches, and navigating websites.\n"
        "  3. 🔍 **Deep Research & Analysis:** Investigating topics, retrieving structured facts, and summarizing data (powered by `researcher`).\n"
        "  4. ✍️ **Content & Technical Writing:** Drafting guides, articles, documentation, summaries, and code solutions (powered by `writer`).\n"
        "  5. 🧐 **Quality Audit & Review:** Auditing drafts for clarity, correctness, edge cases, and executive polish (powered by `reviewer`).\n\n"
        "### CRITICAL ACTION & VISION RULES:\n"
        "1. **Uploaded Images in Chat:** When the user attaches or uploads an image (such as schedules, documents, receipts, screenshots), "
        "YOU AND YOUR AGENTS HAVE NATIVE MULTIMODAL VISION! Read, transcribe, extract, and analyze the image content directly. "
        "DO NOT ask for a file path or claim you cannot see the image!\n"
        "2. **Local Image File Paths:** If the user provides a string path to an image on disk (e.g. 'C:\\docs\\receipt.png'), call `extract_text_from_image` or delegate to `document_ocr_specialist`.\n"
        "3. **Tab Listing & Inspection:** When asked 'how many tabs are open' or 'what tabs are open', call `list_open_browser_tabs`.\n"
        "4. **Browser Navigation & YouTube Searches:** Call `search_youtube` or `open_or_reuse_tab` to prevent duplicate tabs.\n"
        "5. **Close Tabs:** Call `close_browser_tab` when requested.\n"
        "6. **Research Inquiries:** Delegate to `researcher`.\n"
        "7. **Content Drafting:** Delegate to `writer`.\n"
        "8. **Quality Review:** Delegate to `reviewer`.\n"
        "9. **Format Output:** Present all outputs in clean, structured Markdown."
    ),
    tools=[
        list_open_browser_tabs,
        open_or_reuse_tab,
        search_youtube,
        search_google,
        close_browser_tab,
        extract_text_from_image,
    ],
    sub_agents=[
        researcher_agent,
        writer_agent,
        reviewer_agent,
        browser_agent,
        document_agent,
    ],
)
