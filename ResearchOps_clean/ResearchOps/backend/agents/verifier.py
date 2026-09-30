import json

from services.gemini_service import generate_json


def verify(question: str, findings: list[dict], sources: list[dict]) -> dict:
    # Deterministic checks first (no AI, no guessing)
    insufficient = []
    for f in findings:
        if not f["sources"]:
            insufficient.append({"task": f["task"], "reason": "No sources found."})
        elif len(f["sources"]) < 2:
            insufficient.append({"task": f["task"], "reason": "Supported by only one source."})
        elif f["confidence"] == "low":
            insufficient.append({"task": f["task"], "reason": "Sources did not clearly answer the task."})

    # AI cross-check for conflicts and irrelevant sources
    compact_findings = [
        {"id": f["id"], "task": f["task"], "finding": f["finding"], "source_ids": [s["id"] for s in f["sources"]]}
        for f in findings
    ]
    compact_sources = [{"id": s["id"], "title": s["title"], "url": s["url"], "text": s["content"][:500]} for s in sources]

    prompt = f"""You are a strict fact-checking reviewer. Original question: {question}

FINDINGS:
{json.dumps(compact_findings, indent=1)}

SOURCES:
{json.dumps(compact_sources, indent=1)}

Check ONLY using the text above:
1. conflicts: findings or sources that contradict each other (name the finding ids and explain).
2. irrelevant_sources: sources that do not help answer the question.
Do not invent conflicts. If none exist, return empty lists.

Return ONLY JSON:
{{"conflicts": [{{"topic": "...", "details": "...", "finding_ids": ["F1","F2"]}}],
  "irrelevant_sources": [{{"source_id": "S3", "reason": "..."}}],
  "summary": "one or two sentence overall assessment of evidence quality"}}"""

    ai = generate_json(prompt)
    conflicts = ai.get("conflicts", []) or []
    irrelevant = ai.get("irrelevant_sources", []) or []

    by_id = {s["id"]: s for s in sources}
    for item in irrelevant:
        s = by_id.get(item.get("source_id"))
        if s:
            item["title"], item["url"] = s["title"], s["url"]

    issues = len(conflicts) + len(insufficient) + len(irrelevant)
    return {
        "status": "issues_found" if issues else "passed",
        "conflicts": conflicts,
        "insufficient_evidence": insufficient,
        "irrelevant_sources": irrelevant,
        "summary": ai.get("summary", ""),
    }
