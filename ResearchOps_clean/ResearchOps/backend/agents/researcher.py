from services.gemini_service import generate_json, ServiceError
from services.search_service import search


def _clip(text: str, n: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n].rstrip() + "…"


def run_research(tasks: list[dict]):
    """Returns (findings, sources). Sources include 'content' for later agents."""
    sources: dict[str, dict] = {}   # url -> source
    task_sources: dict[int, list[str]] = {}
    first_error = None

    for t in tasks:
        ids = []
        try:
            results = search(t["search_query"])
        except ServiceError as e:
            first_error = first_error or str(e)
            results = []
        for r in results:
            if r["url"] not in sources:
                sources[r["url"]] = {
                    "id": f"S{len(sources) + 1}",
                    "title": r["title"],
                    "url": r["url"],
                    "summary": _clip(r["content"], 300),
                    "content": _clip(r["content"], 1200),
                }
            ids.append(sources[r["url"]]["id"])
        task_sources[t["id"]] = ids

    if not sources:
        raise ServiceError(first_error or "Web search returned no results for any task. Try a broader question.")

    by_id = {s["id"]: s for s in sources.values()}

    # Build one grounded extraction prompt for all tasks that have sources
    blocks = []
    for t in tasks:
        if not task_sources[t["id"]]:
            continue
        lines = [f"TASK {t['id']}: {t['task']}"]
        for sid in task_sources[t["id"]]:
            s = by_id[sid]
            lines.append(f"[{sid}] {s['title']}\n{s['content']}")
        blocks.append("\n".join(lines))

    prompt = f"""You are a research analyst. For each TASK below, write a concise finding (2-4 sentences)
using ONLY the source text provided under that task. Do not add outside knowledge. If the sources do not
answer the task, say so plainly and set confidence to "low". Cite source ids like [S1] inside the finding.

{chr(10).join(blocks)}

Return ONLY JSON:
{{"findings": [{{"task_id": 1, "finding": "...", "confidence": "high|medium|low", "source_ids": ["S1"]}}]}}"""

    extracted = {}
    for f in generate_json(prompt).get("findings", []):
        try:
            extracted[int(f.get("task_id"))] = f
        except (TypeError, ValueError):
            continue

    findings = []
    for t in tasks:
        allowed = task_sources[t["id"]]
        if not allowed:
            findings.append({
                "id": f"F{t['id']}", "task_id": t["id"], "task": t["task"],
                "finding": "No sources were found for this task.",
                "confidence": "none", "sources": [],
            })
            continue
        f = extracted.get(t["id"], {})
        cited = [sid for sid in f.get("source_ids", []) if sid in allowed] or allowed
        findings.append({
            "id": f"F{t['id']}",
            "task_id": t["id"],
            "task": t["task"],
            "finding": str(f.get("finding") or "No finding could be extracted; see the listed sources."),
            "confidence": f.get("confidence") if f.get("confidence") in ("high", "medium", "low") else "low",
            "sources": [
                {k: by_id[sid][k] for k in ("id", "title", "url", "summary")} for sid in cited
            ],
        })
    return findings, list(sources.values())
