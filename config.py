"""Global configuration and environment settings for the multi-agent system."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

# Centralized model setting configurable via .env
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
