import re
import hashlib
import os

SALT = os.environ.get("ANON_SALT", "ml-grader-default")

# ── Anonymization ─────────────────────────────────────────────────────────────

def generate_anon_id(team_name: str, project_number: int) -> str:
    """Consistent short hash for external tracking — never exposes team name."""
    raw = f"{team_name.lower().strip()}:{project_number}:{SALT}"
    return "ANON-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


# ── PII Detection & Redaction ─────────────────────────────────────────────────

_PII_PATTERNS = [
    ("email",      r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'),
    ("phone",      r'\b(\+1[\s\-.]?)?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}\b'),
    ("ssn",        r'\b\d{3}-\d{2}-\d{4}\b'),
    ("student_id", r'\b(ID|id|student\s?id|IWU)?[\s#:]?\d{7,10}\b'),
]


def detect_pii(text: str) -> dict:
    """Returns a report of PII types found and their counts."""
    report = {"detected": False, "types": [], "counts": {}}
    for label, pattern in _PII_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            report["detected"] = True
            report["types"].append(label)
            report["counts"][label] = len(matches)
    return report


def redact_pii(text: str) -> tuple[str, dict]:
    """Returns (redacted_text, pii_report). Safe to send externally."""
    report = detect_pii(text)
    redacted = text
    for label, pattern in _PII_PATTERNS:
        redacted = re.sub(pattern, f"[REDACTED-{label.upper()}]", redacted)
    return redacted, report
