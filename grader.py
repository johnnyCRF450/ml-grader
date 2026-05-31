import anthropic
from rubrics import PROJECTS


def grade_submission(project_number: int, submission_text: str, team_name: str) -> tuple[str, str]:
    project = PROJECTS[project_number]

    client = anthropic.Anthropic()

    system_prompt = f"""You are a grader for a graduate machine learning course. Be thorough, fair, and specific.

PROJECT: {project['name']}

PROJECT DESCRIPTION:
{project['description']}

GRADING RUBRIC:
{project['rubric']}

Evaluate the submission against each rubric criterion. Reference specific parts of the student's work.
Return your response in EXACTLY this format (keep the headers):

GRADE: [letter grade A+ / A / A- / B+ / B / B- / C+ / C / C- / D / F]

SUMMARY:
[2-3 sentence overall assessment]

RUBRIC BREAKDOWN:
[For each criterion in the rubric: criterion name, score/assessment, specific feedback]

STRENGTHS:
[2-3 specific things done well, with examples from the submission]

AREAS FOR IMPROVEMENT:
[2-3 specific, actionable suggestions]"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Team: {team_name}\n\nSubmission content:\n\n{submission_text[:15000]}"
        }]
    )

    response = message.content[0].text

    grade = "N/A"
    for line in response.split("\n"):
        if line.startswith("GRADE:"):
            grade = line.replace("GRADE:", "").strip()
            break

    return grade, response


def grade_all_pending(submissions: list, progress_callback=None) -> list[dict]:
    results = []
    for i, sub in enumerate(submissions):
        if sub["status"] != "pending":
            continue
        if progress_callback:
            progress_callback(i, sub["team_name"], sub["project_number"])
        try:
            from extractor import extract_text
            text = extract_text(sub["file_path"])
            grade, feedback = grade_submission(sub["project_number"], text, sub["team_name"])
            results.append({"id": sub["id"], "grade": grade, "feedback": feedback, "error": None})
        except Exception as e:
            results.append({"id": sub["id"], "grade": "", "feedback": "", "error": str(e)})
    return results
