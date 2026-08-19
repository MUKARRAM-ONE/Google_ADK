"""Document & OCR Sub-Agent: Extracts and analyzes text from images and documents."""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import Agent
from config import DEFAULT_MODEL

try:
    from tools.ocr_tools import extract_text_from_image
except ImportError:
    from ..tools.ocr_tools import extract_text_from_image

document_agent = Agent(
    name="document_ocr_specialist",
    model=DEFAULT_MODEL,
    description=(
        "Specialist in document analysis, image text extraction, and OCR. "
        "Use this agent when the user uploads an image, schedule, receipt, document, or provides an image file path."
    ),
    instruction=(
        "You are an expert Document & Multimodal Image Specialist.\n\n"
        "### How to Handle Images & Documents:\n"
        "1. **Uploaded Images in Chat:** When the user uploads or attaches an image directly in the conversation, "
        "YOU CAN SEE THE IMAGE DIRECTLY via your native multimodal vision! Immediately read, transcribe, and analyze "
        "all text, schedules, tables, headers, and bullet points from the image. NEVER ask the user for a file path when they already attached/uploaded the image!\n"
        "2. **Local File Paths:** If the user specifies a local file path on disk (e.g. 'C:\\path\\to\\image.png'), "
        "call the `extract_text_from_image` tool to read the file.\n"
        "3. **Output Format:** Present the extracted information clearly with clean Markdown formatting (tables, bullet points, headers) and answer any questions the user asked."
    ),
    tools=[extract_text_from_image],
)
