"""Tesseract OCR and Document Image Extraction Tools for Google ADK."""
import os
import shutil
from pathlib import Path
from PIL import Image
import pytesseract
from dotenv import load_dotenv

load_dotenv()

def _find_tesseract_binary() -> str | None:
    """Detects tesseract.exe path from PATH, .env, or common Windows locations."""
    custom_path = os.getenv("TESSERACT_CMD")
    if custom_path and os.path.exists(custom_path):
        return custom_path
        
    which_path = shutil.which("tesseract")
    if which_path:
        return which_path
        
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LocalAppData%\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expandvars(r"%ProgramW6432%\Tesseract-OCR\tesseract.exe"),
    ]
    
    for p in common_paths:
        if os.path.exists(p):
            return p
            
    return None


def extract_text_from_image(image_path: str) -> dict:
    """Extracts raw and structured text from an image file (PNG, JPG, TIFF, BMP) or scanned document using Tesseract OCR.
    
    Args:
        image_path: The local absolute or relative file path to the image/document.
        
    Returns:
        A dictionary containing the extracted text and execution details.
    """
    resolved_path = Path(image_path).expanduser().resolve()
    
    if not resolved_path.exists():
        return {
            "status": "error",
            "message": f"Image file not found at: {image_path}"
        }
        
    tess_binary = _find_tesseract_binary()
    if tess_binary:
        pytesseract.pytesseract.tesseract_cmd = tess_binary
    else:
        return {
            "status": "missing_engine",
            "message": (
                "Tesseract OCR binary (tesseract.exe) was not found. "
                "To enable local OCR, install Tesseract via PowerShell: `winget install UB-Mannheim.TesseractOCR` "
                "or set TESSERACT_CMD in your .env file."
            )
        }
        
    try:
        with Image.open(resolved_path) as img:
            extracted = pytesseract.image_to_string(img)
            
        clean_text = extracted.strip()
        lines = [line for line in clean_text.splitlines() if line.strip()]
        
        return {
            "status": "success",
            "file": str(resolved_path),
            "line_count": len(lines),
            "extracted_text": clean_text if clean_text else "(No readable text detected in the image)",
            "message": f"Successfully extracted {len(lines)} line(s) of text from image."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to perform OCR on {image_path}: {str(e)}"
        }
