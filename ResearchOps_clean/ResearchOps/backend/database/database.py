import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "researchops.db"


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _conn() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS research_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                created_at TEXT NOT NULL,
                final_report TEXT NOT NULL
            )"""
        )


def save_session(question: str, final_report: str) -> int:
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO research_sessions (question, created_at, final_report) VALUES (?, ?, ?)",
            (question, datetime.now(timezone.utc).isoformat(), final_report),
        )
        return cur.lastrowid


def list_sessions(limit: int = 20):
    with _conn() as c:
        rows = c.execute(
            "SELECT id, question, created_at, final_report FROM research_sessions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [{"id": r[0], "question": r[1], "created_at": r[2], "final_report": r[3]} for r in rows]
