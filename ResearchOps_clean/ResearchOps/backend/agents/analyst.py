import json

from services.gemini_service import generate_json


def analyze(question: str, findings: list[dict], verification: dict) -> dict:
    compact = [
        {"id": f["id"], "task": f["task"], "finding": f["finding"],
         "confidence": f["confidence"], "source_ids": [s["id"] for s in f["sources"]]}
        for f in findings
    ]
    prompt = f"""You are a senior research analyst. Write an analysis answering the question, using ONLY
the findings below. Do not invent facts, numbers, or sources. Cite source ids like [S1] where relevant.
Respect the verification results: mention conflicts and weak evidence honestly; do not overstate.

QUESTION: {question}

FINDINGS:
{json.dumps(compact, indent=1)}

VERIFICATION:
{json.dumps(verification, indent=1)}

Return ONLY JSON:
{{"executive_summary": "3-5 sentences",
  "key_findings": ["bullet", "bullet"],
  "comparison": "a paragraph comparing options/perspectives/approaches found in the evidence",
  "opportunities": ["bullet"],
  "risks": ["bullet"],
  "conclusion": "2-4 sentences"}}"""

    data = generate_json(prompt)
    as_list = lambda v: [str(x) for x in v] if isinstance(v, list) else ([str(v)] if v else [])
    return {
        "executive_summary": str(data.get("executive_summary", "")),
        "key_findings": as_list(data.get("key_findings")),
        "comparison": str(data.get("comparison", "")),
        "opportunities": as_list(data.get("opportunities")),
        "risks": as_list(data.get("risks")),
        "conclusion": str(data.get("conclusion", "")),
    }
