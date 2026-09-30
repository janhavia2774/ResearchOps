import json
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class ServiceError(Exception):
    """Raised when an external API fails or returns unusable data."""


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def _call_gemini(prompt: str, json_mode: bool) -> str:
    key = os.getenv("GEMINI_API_KEY", "")
    if not key or key.startswith("your_"):
        raise ServiceError("GEMINI_API_KEY is missing. Add it to backend/.env")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    config = {"temperature": 0.2}
    if json_mode:
        config["responseMimeType"] = "application/json"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": config}
    headers = {"Content-Type": "application/json", "x-goog-api-key": key}

    last_error = "unknown error"
    for attempt in range(3):
        try:
            resp = requests.post(GEMINI_URL.format(model=model), json=payload, headers=headers, timeout=120)
        except requests.RequestException as e:
            last_error = f"network error: {e}"
            time.sleep(2 * (attempt + 1))
            continue

        if resp.status_code == 200:
            try:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, ValueError):
                raise ServiceError("Gemini returned an empty or blocked response.")

        try:
            last_error = resp.json().get("error", {}).get("message", resp.text[:200])
        except ValueError:
            last_error = resp.text[:200]

        if resp.status_code in (429, 500, 503):  # transient: retry
            time.sleep(3 * (attempt + 1))
            continue
        break

    raise ServiceError(f"Gemini API error: {last_error}")


def generate_text(prompt: str) -> str:
    return _call_gemini(prompt, json_mode=False)


def generate_json(prompt: str) -> dict:
    for attempt in range(2):
        raw = _call_gemini(prompt, json_mode=True)
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    raise ServiceError("Gemini did not return valid JSON. Please try again.")
