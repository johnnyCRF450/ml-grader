import anthropic
from rubrics import PROJECTS
from syllabus import OUTCOMES, keyword_precheck
from privacy import redact_pii

MODEL = "claude-sonnet-4-6"


# ── Response parsers ──────────────────────────────────────────────────────────

def _parse_criterion_scores(response: str) -> dict:
    """Parse the CRITERION_SCORES block into a dict keyed by criterion name."""
    scores = {}
    in_block = False
    for line in response.split("\n"):
        stripped = line.strip()
        if stripped == "CRITERION_SCORES:":
            in_block = True
            continue
        if in_block:
            if stripped == "" or stripped.startswith(("SYLLABUS_ALIGNMENT", "GRADE:", "SUMMARY", "RAI_FLAGS")):
                break
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 2:
                criterion = parts[0]
                score_raw = parts[1]   # "18 / 20"
                justification = parts[2] if len(parts) > 2 else ""
                try:
                    score_str, max_str = score_raw.split("/")
                    scores[criterion] = {
                        "score": int(score_str.strip()),
                        "max":   int(max_str.strip()),
                        "justification": justification,
                    }
                except (ValueError, IndexError):
                    pass
    return scores


def _parse_syllabus_alignment(response: str) -> dict:
    """Parse the SYLLABUS_ALIGNMENT block."""
    result = {"score": 0, "met": [], "missing": []}
    in_block = False
    for line in response.split("\n"):
        stripped = line.strip()
        if stripped == "SYLLABUS_ALIGNMENT:":
            in_block = True
            continue
        if in_block:
            if stripped == "" and result["score"] > 0:
                break
            if stripped.startswith("GRADE:") or stripped.startswith("SUMMARY"):
                break
            if stripped.startswith("SCORE:"):
                try:
                    result["score"] = int(stripped.replace("SCORE:", "").strip())
                except ValueError:
                    pass
            elif stripped.startswith("MET:"):
                raw = stripped.replace("MET:", "").strip()
                result["met"] = [x.strip() for x in raw.split(";") if x.strip()]
            elif stripped.startswith("MISSING:"):
                raw = stripped.replace("MISSING:", "").strip()
                result["missing"] = [x.strip() for x in raw.split(";") if x.strip()]
    return result


def _parse_rai_flags(response: str) -> list[str]:
    flags = []
    in_block = False
    for line in response.split("\n"):
        stripped = line.strip()
        if stripped == "RAI_FLAGS:":
            in_block = True
            continue
        if in_block:
            if stripped == "" or stripped.startswith("GRADE:"):
                break
            if stripped and stripped.lower() not in ("none", "none detected", "none identified"):
                flags.append(stripped.lstrip("- "))
    return flags


def _parse_grade(response: str) -> str:
    for line in response.split("\n"):
        if line.strip().startswith("GRADE:"):
            return line.replace("GRADE:", "").strip()
    return "N/A"


# ── Main grading function ────────────────────────────────────────────────────

def grade_submission(project_number: int, submission_text: str,
                     team_name: str, anon_id: str = "ANON") -> dict:
    """
    Returns a dict with all grading outputs.
    Uses anon_id externally — never sends raw team_name to the API.
    PII is redacted from submission text before the API call.
    """
    project = PROJECTS[project_number]
    outcomes = OUTCOMES.get(project_number, {})
    outcomes_list = outcomes.get("outcomes", [])

    # Privacy: redact PII before sending externally
    clean_text, pii_report = redact_pii(submission_text)

    # Syllabus: fast keyword pre-check (no API call)
    precheck = keyword_precheck(clean_text, project_number)

    outcomes_str = "\n".join(f"  - {o}" for o in outcomes_list)

    system_prompt = f"""You are a grader for a graduate machine learning course (AIML-501: Model Development).
Be thorough, fair, specific, and consistent.

PROJECT: {project['name']}

PROJECT DESCRIPTION:
{project['description']}

GRADING RUBRIC:
{project['rubric']}

COURSE LEARNING OUTCOMES FOR THIS PROJECT:
{outcomes_str}

KEYWORD PRE-SCAN (topics detected in submission):
  Matched ({precheck['coverage_pct']}% coverage): {', '.join(precheck['matched']) or 'none'}
  Potentially missing: {', '.join(precheck['missing']) or 'none'}

RESPONSIBLE AI NOTE: Flag any concerns about bias, fairness, equity, or ethical issues in the student's work.

Return your response in EXACTLY this format. Keep all headers. Do not add extra sections.

CRITERION_SCORES:
[criterion name] | [score] / [max] | [one-line justification]
(one line per rubric criterion)

SYLLABUS_ALIGNMENT:
SCORE: [0-100]
MET: [semicolon-separated list of met learning outcomes, or 'None']
MISSING: [semicolon-separated list of unmet learning outcomes, or 'None']

RAI_FLAGS:
[List any responsible AI concerns: bias in problem framing, ethical issues, privacy concerns, or 'None']

GRADE: [A+ / A / A- / B+ / B / B- / C+ / C / C- / D / F]

SUMMARY:
[2-3 sentence overall assessment]

RUBRIC BREAKDOWN:
[For each criterion: name, detailed feedback referencing specific parts of the submission]

STRENGTHS:
[2-3 specific things done well with examples from the submission]

AREAS FOR IMPROVEMENT:
[2-3 specific, actionable suggestions]"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Submission ID: {anon_id}\n\nSubmission content:\n\n{clean_text[:15000]}"
        }]
    )

    response = message.content[0].text

    return {
        "grade":            _parse_grade(response),
        "feedback":         response,
        "criterion_scores": _parse_criterion_scores(response),
        "syllabus_score":   _parse_syllabus_alignment(response)["score"],
        "syllabus_met":     _parse_syllabus_alignment(response)["met"],
        "syllabus_missing": _parse_syllabus_alignment(response)["missing"],
        "rai_flags":        _parse_rai_flags(response),
        "pii_detected":     pii_report["detected"],
        "pii_types":        pii_report["types"],
        "input_chars":      len(clean_text),
        "output_chars":     len(response),
        "model_used":       MODEL,
    }
