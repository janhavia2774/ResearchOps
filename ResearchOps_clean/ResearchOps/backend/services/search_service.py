import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from services.gemini_service import ServiceError

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TAVILY_URL = "https://api.tavily.com/search"


def search(query: str, max_results: int = 4) -> list[dict]:
    """Search Tavily. Returns [{title, url, content}]. Empty list if nothing found."""
    key = os.getenv("TAVILY_API_KEY", "")
    if not key or key.startswith("your_"):
        raise ServiceError("TAVILY_API_KEY is missing. Add it to backend/.env")

    try:
        resp = requests.post(
            TAVILY_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"query": query, "max_results": max_results, "search_depth": "basic"},
            timeout=45,
        )
    except requests.RequestException as e:
        raise ServiceError(f"Tavily network error: {e}")

    if resp.status_code != 200:
        raise ServiceError(f"Tavily API error {resp.status_code}: {resp.text[:200]}")

    results = []
    for r in resp.json().get("results", []):
        if r.get("url") and r.get("content"):
            results.append({
                "title": r.get("title") or r["url"],
                "url": r["url"],
                "content": r["content"],
            })
    return results
