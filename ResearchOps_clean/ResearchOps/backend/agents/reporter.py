def _bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "- None identified from the evidence."


def _safe(text: str) -> str:
    return text.replace("[", "(").replace("]", ")")


def build_report(question: str, analysis: dict, verification: dict, sources: list[dict]) -> str:
    v = verification
    notes = []
    for c in v.get("conflicts", []):
        notes.append(f"Conflict: {c.get('topic', '')} — {c.get('details', '')}")
    for e in v.get("insufficient_evidence", []):
        notes.append(f"Weak evidence: {e.get('task', '')} — {e.get('reason', '')}")
    for i in v.get("irrelevant_sources", []):
        notes.append(f"Irrelevant source {i.get('source_id', '')}: {i.get('reason', '')}")
    if v.get("summary"):
        notes.insert(0, v["summary"])

    source_lines = "\n".join(
        f"- {s['id']}: [{_safe(s['title'])}]({s['url']})" for s in sources
    )

    return f"""# Research Report

## Question
{question}

## Executive Summary
{analysis['executive_summary']}

## Key Findings
{_bullets(analysis['key_findings'])}

## Comparison
{analysis['comparison']}

## Opportunities
{_bullets(analysis['opportunities'])}

## Risks
{_bullets(analysis['risks'])}

## Conclusion
{analysis['conclusion']}

## Verification Notes
{_bullets(notes)}

## Sources
{source_lines}
"""
