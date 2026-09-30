from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents import planner, researcher, verifier, analyst, reporter
from database.database import init_db, save_session, list_sessions
from services.gemini_service import ServiceError

app = FastAPI(title="ResearchOps AI")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?|https://janhavia2774\.github\.io",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=1000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history")
def history():
    return list_sessions()


@app.post("/research")
def research(req: ResearchRequest):
    question = req.question.strip()
    try:
        tasks = planner.plan(question)
        findings, full_sources = researcher.run_research(tasks)
        verification = verifier.verify(question, findings, full_sources)
        analysis = analyst.analyze(question, findings, verification)
        final_report = reporter.build_report(question, analysis, verification, full_sources)
    except ServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    save_session(question, final_report)

    return {
        "question": question,
        "research_tasks": tasks,
        "findings": findings,
        "verification": verification,
        "analysis": analysis,
        "final_report": final_report,
        "sources": [{k: s[k] for k in ("id", "title", "url", "summary")} for s in full_sources],
    }
