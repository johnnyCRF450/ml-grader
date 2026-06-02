import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/grader.db")


def init_audit_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                anon_id TEXT NOT NULL,
                submission_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                model_used TEXT,
                input_chars INTEGER,
                output_chars INTEGER,
                ai_grade TEXT,
                pii_detected INTEGER DEFAULT 0,
                pii_types TEXT DEFAULT '[]',
                syllabus_score INTEGER,
                human_modified INTEGER DEFAULT 0,
                final_grade TEXT,
                notes TEXT,
                FOREIGN KEY (submission_id) REFERENCES submissions(id)
            )
        """)
        conn.commit()


def log_event(submission_id: int, anon_id: str, event_type: str, **kwargs):
    """
    event_type: 'submitted' | 'graded' | 'approved'
    kwargs: model_used, input_chars, output_chars, ai_grade, pii_detected,
            pii_types (list), syllabus_score, human_modified, final_grade, notes
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO audit_log
            (timestamp, anon_id, submission_id, event_type, model_used,
             input_chars, output_chars, ai_grade, pii_detected, pii_types,
             syllabus_score, human_modified, final_grade, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            anon_id,
            submission_id,
            event_type,
            kwargs.get("model_used"),
            kwargs.get("input_chars"),
            kwargs.get("output_chars"),
            kwargs.get("ai_grade"),
            int(bool(kwargs.get("pii_detected", False))),
            json.dumps(kwargs.get("pii_types", [])),
            kwargs.get("syllabus_score"),
            int(bool(kwargs.get("human_modified", False))),
            kwargs.get("final_grade"),
            kwargs.get("notes"),
        ))


def get_audit_trail(submission_id: int) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM audit_log WHERE submission_id = ? ORDER BY timestamp ASC",
            (submission_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_all_audit_logs() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM audit_log ORDER BY timestamp DESC"
        ).fetchall()
        return [dict(r) for r in rows]
