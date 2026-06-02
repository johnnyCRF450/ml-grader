import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/grader.db")


def _migrate(conn):
    """Add new columns to existing DB without wiping data."""
    new_columns = [
        ("anon_id",            "TEXT"),
        ("criterion_scores",   "TEXT"),
        ("syllabus_score",     "INTEGER"),
        ("syllabus_met",       "TEXT"),
        ("syllabus_missing",   "TEXT"),
        ("pii_detected",       "INTEGER DEFAULT 0"),
        ("pii_types",          "TEXT DEFAULT '[]'"),
    ]
    existing = {row[1] for row in conn.execute("PRAGMA table_info(submissions)").fetchall()}
    for col, col_type in new_columns:
        if col not in existing:
            conn.execute(f"ALTER TABLE submissions ADD COLUMN {col} {col_type}")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL,
                project_number INTEGER NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                anon_id TEXT,
                ai_grade TEXT,
                ai_feedback TEXT,
                criterion_scores TEXT,
                syllabus_score INTEGER,
                syllabus_met TEXT,
                syllabus_missing TEXT,
                pii_detected INTEGER DEFAULT 0,
                pii_types TEXT DEFAULT '[]',
                final_grade TEXT,
                final_feedback TEXT,
                approved_at TEXT
            )
        """)
        _migrate(conn)

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


def add_submission(team_name, project_number, filename, file_path, anon_id=None):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """INSERT INTO submissions
               (team_name, project_number, filename, file_path, submitted_at, anon_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (team_name, project_number, filename, file_path,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), anon_id)
        )
        return cur.lastrowid


def get_all_submissions():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute(
            "SELECT * FROM submissions ORDER BY project_number, team_name, submitted_at DESC"
        ).fetchall()]


def get_submission(sub_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,)).fetchone()
        return dict(row) if row else None


def save_ai_grade(sub_id, ai_grade, ai_feedback,
                  criterion_scores=None, syllabus_score=None,
                  syllabus_met=None, syllabus_missing=None,
                  pii_detected=False, pii_types=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """UPDATE submissions SET
               ai_grade = ?, ai_feedback = ?, status = 'ai_graded',
               criterion_scores = ?, syllabus_score = ?,
               syllabus_met = ?, syllabus_missing = ?,
               pii_detected = ?, pii_types = ?
               WHERE id = ?""",
            (
                ai_grade, ai_feedback,
                json.dumps(criterion_scores or {}),
                syllabus_score,
                json.dumps(syllabus_met or []),
                json.dumps(syllabus_missing or []),
                int(bool(pii_detected)),
                json.dumps(pii_types or []),
                sub_id,
            )
        )


def approve_grade(sub_id, final_grade, final_feedback):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """UPDATE submissions SET
               final_grade = ?, final_feedback = ?,
               status = 'approved', approved_at = ?
               WHERE id = ?""",
            (final_grade, final_feedback,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sub_id)
        )
