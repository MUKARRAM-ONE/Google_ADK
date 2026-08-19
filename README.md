# Google ADK Multi-Agent System

An interactive Multi-Agent system built with the [Google Agent Development Kit (ADK)](https://adk.dev/) and powered by Google Gemini.

## Architecture

```
User <---> Coordinator Assistant (Root Agent)
                 |
                 +--> Document & OCR Specialist (Extracts text from images & PDFs via Tesseract)
                 |
                 +--> Browser Operator (Tab-aware: lists tabs, reuses tabs, searches YouTube/Google)
                 |
                 +--> Researcher Sub-Agent (Gathers facts, reads web URLs)
                 |
                 +--> Writer Sub-Agent (Drafts structured content & code)
                 |
                 +--> Reviewer Sub-Agent (Audits, polishes & QA)
```

## Project Structure

```text
Google_ADK/
├── .env                     # GEMINI_API_KEY, GEMINI_MODEL, TESSERACT_CMD
├── pyproject.toml           # uv project configuration
├── config.py                # Centralized model and environment loader
├── tools/
│   ├── __init__.py
│   ├── browser_tools.py     # Tab listing, duplicate prevention, YouTube/Google
│   ├── ocr_tools.py         # Tesseract OCR extraction from images/documents
│   └── search_tools.py      # Knowledge base search and URL scraper
├── sub_agents/
│   ├── __init__.py
│   ├── browser_agent.py     # Browser & navigation operator
│   ├── document_agent.py    # Document & OCR specialist
│   ├── researcher.py        # Information & fact retrieval agent
│   ├── writer.py            # Content drafting agent
│   └── reviewer.py          # QA, audit & editing agent
└── agent.py                 # Root Coordinator (root_agent)
```

## Optional: Installing Tesseract OCR Engine

To enable offline OCR on Windows:
```powershell
winget install UB-Mannheim.TesseractOCR
```
Or download the installer from [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki).

## Running the Agent

### Start the Interactive Web UI
```bash
uv run adk web
```
Open `http://127.0.0.1:8000` in your browser.

---

### Example Prompts:
* *"Hey"*
* *"Extract text from this image: C:\path\to\receipt.png"*
* *"How many tabs are open in my browser?"*
* *"Open YouTube and search for coding music"*
* *"Research the latest Google ADK multi-agent features"*
