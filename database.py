import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/grader.db")


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
                ai_grade TEXT,
                ai_feedback TEXT,
                final_grade TEXT,
                final_feedback TEXT,
                approved_at TEXT
            )
        """)
        conn.commit()


def add_submission(team_name, project_number, filename, file_path):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO submissions (team_name, project_number, filename, file_path, submitted_at) VALUES (?, ?, ?, ?, ?)",
            (team_name, project_number, filename, file_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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


def save_ai_grade(sub_id, ai_grade, ai_feedback):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE submissions SET ai_grade = ?, ai_feedback = ?, status = 'ai_graded' WHERE id = ?",
            (ai_grade, ai_feedback, sub_id)
        )


def approve_grade(sub_id, final_grade, final_feedback):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE submissions SET final_grade = ?, final_feedback = ?, status = 'approved', approved_at = ? WHERE id = ?",
            (final_grade, final_feedback, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sub_id)
        )
