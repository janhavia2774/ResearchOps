from services.gemini_service import generate_json, ServiceError


def plan(question: str) -> list[dict]:
    prompt = f"""You are a research planner. Break the research question below into 5 to 7 specific,
distinct research tasks that together fully answer it. Each task needs a web search query.

Research question: {question}

Return ONLY JSON in this format:
{{"tasks": [{{"id": 1, "task": "clear description of what to find out", "search_query": "concise web search query"}}]}}"""

    data = generate_json(prompt)
    tasks = []
    for i, t in enumerate(data.get("tasks", [])[:7], start=1):
        task = str(t.get("task", "")).strip()
        if task:
            tasks.append({
                "id": i,
                "task": task,
                "search_query": str(t.get("search_query") or task).strip(),
            })
    if not tasks:
        raise ServiceError("Planner could not generate research tasks. Try rephrasing the question.")
    return tasks
