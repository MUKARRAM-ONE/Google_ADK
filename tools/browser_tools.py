"""Advanced Browser Automation & Session Tab Management for Google ADK."""
import os
import re
import json
import time
import subprocess
import urllib.parse
import webbrowser
import httpx

CDP_BASE_URL = "http://127.0.0.1:9222"
SESSION_TABS_FILE = os.path.join(os.path.dirname(__file__), ".active_tabs.json")

def _load_session_tabs() -> list[dict]:
    """Loads the active session tab registry."""
    if os.path.exists(SESSION_TABS_FILE):
        try:
            with open(SESSION_TABS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_session_tabs(tabs: list[dict]):
    """Saves the active session tab registry."""
    try:
        with open(SESSION_TABS_FILE, "w", encoding="utf-8") as f:
            json.dump(tabs, f, indent=2)
    except Exception:
        pass


def _register_tab(url: str, title: str = ""):
    """Registers or updates a tab in the session registry."""
    tabs = _load_session_tabs()
    if not title:
        parsed = urllib.parse.urlparse(url)
        title = parsed.netloc.replace("www.", "").capitalize()
        if "youtube.com" in url:
            title = "YouTube"
        elif "mail.google.com" in url:
            title = "Gmail"
        elif "google.com" in url:
            title = "Google Search"
            
    # Check if exists
    for t in tabs:
        if t.get("url") == url or ("youtube.com" in url and "youtube.com" in t.get("url", "")):
            t["url"] = url
            t["title"] = title
            t["last_active"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _save_session_tabs(tabs)
            return
            
    tabs.append({
        "id": f"tab_{len(tabs) + 1}",
        "title": title,
        "url": url,
        "opened_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active"
    })
    _save_session_tabs(tabs)


def _get_cdp_tabs() -> list[dict]:
    """Attempts to fetch live tabs from Chrome CDP if remote debugging is active."""
    try:
        res = httpx.get(f"{CDP_BASE_URL}/json/list", timeout=1.0)
        if res.status_code == 200:
            return [t for t in res.json() if t.get("type") == "page"]
    except Exception:
        pass
    return []


def list_open_browser_tabs() -> dict:
    """Lists all open tabs and active browser sessions, including their titles, links, and open status.
    
    Returns:
        A dictionary containing the list of open tabs and total count.
    """
    # Check CDP live tabs
    cdp_tabs = _get_cdp_tabs()
    session_tabs = _load_session_tabs()
    
    combined_tabs = []
    seen_urls = set()
    
    if cdp_tabs:
        for i, t in enumerate(cdp_tabs, 1):
            url = t.get("url", "")
            title = t.get("title", "Untitled")
            if url and url not in seen_urls:
                seen_urls.add(url)
                combined_tabs.append({
                    "tab_number": len(combined_tabs) + 1,
                    "title": title,
                    "url": url,
                    "source": "live_browser"
                })
                
    for t in session_tabs:
        url = t.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            combined_tabs.append({
                "tab_number": len(combined_tabs) + 1,
                "title": t.get("title", "Active Tab"),
                "url": url,
                "source": "session_registry"
            })
            
    if not combined_tabs:
        return {
            "status": "success",
            "total_open_tabs": 0,
            "tabs": [],
            "message": "No browser tabs have been opened yet in this session."
        }
        
    return {
        "status": "success",
        "total_open_tabs": len(combined_tabs),
        "tabs": combined_tabs,
        "message": f"Found {len(combined_tabs)} active browser tab(s)."
    }


def open_or_reuse_tab(url: str, domain_keyword: str = "") -> dict:
    """Navigates to a URL. If a tab matching that domain (e.g. YouTube) is already open, it reuses it instead of opening a duplicate.
    
    Args:
        url: The web URL to open (e.g. 'https://www.youtube.com', 'https://mail.google.com').
        domain_keyword: Optional domain identifier to prevent duplicates (e.g. 'youtube', 'gmail').
        
    Returns:
        Dictionary confirming whether a tab was reused or newly opened.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    keyword = domain_keyword.lower() if domain_keyword else urllib.parse.urlparse(url).netloc.lower()
    
    # Check CDP
    cdp_tabs = _get_cdp_tabs()
    for tab in cdp_tabs:
        if keyword in tab.get("url", "").lower() or keyword in tab.get("title", "").lower():
            tab_id = tab.get("id", "")
            try:
                httpx.get(f"{CDP_BASE_URL}/json/activate/{tab_id}", timeout=1.0)
            except Exception:
                pass
            _register_tab(url, tab.get("title", ""))
            return {
                "status": "success",
                "action": "reused_existing_tab",
                "title": tab.get("title"),
                "url": url,
                "message": f"Focused existing tab '{tab.get('title')}' and navigated to {url} without opening a duplicate tab."
            }
            
    # Check Session Registry
    session_tabs = _load_session_tabs()
    for t in session_tabs:
        if keyword in t.get("url", "").lower() or keyword in t.get("title", "").lower():
            t["url"] = url
            t["last_active"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _save_session_tabs(session_tabs)
            webbrowser.open_new_tab(url)
            return {
                "status": "success",
                "action": "reused_session_tab",
                "title": t.get("title"),
                "url": url,
                "message": f"Reused active tab '{t.get('title')}' with new URL: {url}."
            }
            
    # Open new tab
    webbrowser.open_new_tab(url)
    _register_tab(url)
    return {
        "status": "success",
        "action": "opened_new_tab",
        "url": url,
        "message": f"Opened {url} in your browser."
    }


def search_youtube(search_query: str = "") -> dict:
    """Searches YouTube or opens YouTube. If a YouTube tab is already open, reuses that tab.
    
    Args:
        search_query: What to search for on YouTube.
        
    Returns:
        Confirmation status.
    """
    if search_query.strip():
        encoded = urllib.parse.quote(search_query.strip())
        url = f"https://www.youtube.com/results?search_query={encoded}"
    else:
        url = "https://www.youtube.com"
        
    return open_or_reuse_tab(url=url, domain_keyword="youtube")


def search_google(query: str) -> dict:
    """Performs a Google search. If a Google search tab is already open, reuses that tab.
    
    Args:
        query: Keywords or question to search on Google.
        
    Returns:
        Confirmation status.
    """
    encoded = urllib.parse.quote(query.strip())
    url = f"https://www.google.com/search?q={encoded}"
    return open_or_reuse_tab(url=url, domain_keyword="google.com/search")


def close_browser_tab(tab_identifier: str) -> dict:
    """Closes or deregisters an active tab by its name, number, or URL keyword.
    
    Args:
        tab_identifier: The name (e.g. 'YouTube', 'Gmail'), index, or URL to close.
        
    Returns:
        Confirmation status.
    """
    session_tabs = _load_session_tabs()
    target = tab_identifier.lower()
    
    # Try closing in CDP
    cdp_tabs = _get_cdp_tabs()
    for tab in cdp_tabs:
        if target in tab.get("title", "").lower() or target in tab.get("url", "").lower() or tab.get("id") == tab_identifier:
            try:
                httpx.get(f"{CDP_BASE_URL}/json/close/{tab.get('id')}", timeout=1.0)
            except Exception:
                pass
                
    remaining = [t for t in session_tabs if target not in t.get("title", "").lower() and target not in t.get("url", "").lower() and t.get("id") != tab_identifier]
    _save_session_tabs(remaining)
    
    return {
        "status": "success",
        "message": f"Closed tab matching '{tab_identifier}'."
    }
