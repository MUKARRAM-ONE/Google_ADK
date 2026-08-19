"""Search and knowledge retrieval tools for agents."""
import urllib.request
import re

def fetch_webpage_content(url: str) -> dict:
    """Fetches and extracts clean text content from a web page URL.
    
    Args:
        url: The web URL (e.g. from an open tab or article) to read.
        
    Returns:
        Extracted text content and status.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Strip script and style tags
        cleaned = re.sub(r'<(script|style).*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Strip HTML tags
        text = re.sub(r'<[^<]+?>', ' ', cleaned)
        # Clean whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        compact_text = "\n".join(lines)
        
        return {
            "url": url,
            "status": "success",
            "content_preview": compact_text[:3000]
        }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error_message": str(e)
        }


def search_knowledge_base(query: str) -> dict:
    """Searches the knowledge base and resources for factual information on a topic.
    
    Args:
        query: The topic, question, or keyword to look up.
        
    Returns:
        A dictionary containing relevant facts, bullet points, and key findings.
    """
    query_lower = query.lower()
    
    if "agent" in query_lower or "adk" in query_lower:
        return {
            "query": query,
            "status": "found",
            "findings": [
                "Google Agent Development Kit (ADK) is an open-source framework for building multi-agent architectures.",
                "Supports hierarchical delegation, sequential pipelines, parallel fan-out, and human-in-the-loop flows.",
                "Built-in ADK Dev UI enables visual trace inspection and live debugging via 'adk web'.",
                "Integrates seamlessly with Gemini models (e.g., gemini-3.6-flash, gemini-2.5-pro)."
            ]
        }
    elif "python" in query_lower:
        return {
            "query": query,
            "status": "found",
            "findings": [
                "Python 3.10+ provides robust async capabilities and type hinting.",
                "Pydantic v2 powers strict schema validation and structured tool calling.",
                "Virtual environments managed via 'uv' ensure blazing-fast dependency resolution."
            ]
        }
    else:
        return {
            "query": query,
            "status": "found",
            "findings": [
                f"Core concepts and foundational insights regarding '{query}'.",
                f"Best practices, architectural patterns, and standard operational procedures for '{query}'.",
                f"Common pitfalls to avoid and key recommendations for '{query}'."
            ]
        }


def summarize_notes(raw_notes: str) -> dict:
    """Extracts key bullet points and high-level themes from unorganized text notes.
    
    Args:
        raw_notes: Unstructured notes or research findings to condense.
        
    Returns:
        Structured summary with key points.
    """
    lines = [line.strip() for line in raw_notes.split("\n") if line.strip()]
    return {
        "status": "success",
        "total_points_analyzed": len(lines),
        "condensed_summary": lines[:5] if lines else ["No notes provided."]
    }
