import streamlit as st
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

import database as db
import extractor
import grader
import audit
import overview
from rubrics import PROJECTS
from privacy import generate_anon_id

SUBMISSIONS_DIR = Path("data/submissions")
SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
db.init_db()
audit.init_audit_table()

INSTRUCTOR_PIN = os.environ.get("GRADER_PIN", "1234")

STATUS_COLORS = {
    "pending":   "🔵",
    "ai_graded": "🟡",
    "approved":  "🟢",
}


def _grade_color(score, max_score):
    pct = score / max_score if max_score else 0
    if pct >= 0.90:
        return "green"
    if pct >= 0.75:
        return "orange"
    return "red"


st.set_page_config(page_title="ML Project Grader", layout="wide", page_icon="🎓")

# ── Sidebar navigation ────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🎓 ML Grader")
    page = st.radio(
        "",
        ["📚 Course Overview", "📤 Submit Project", "📊 Instructor Dashboard"],
        label_visibility="collapsed"
    )
    st.divider()
    if page == "📊 Instructor Dashboard":
        pin = st.text_input("Instructor PIN", type="password", placeholder="Enter PIN")
        if pin and pin != INSTRUCTOR_PIN:
            st.error("Incorrect PIN")
            st.stop()
        elif not pin:
            st.info("Enter PIN to access dashboard")
            st.stop()


# ════════════════════════════════════════════════════════════════════════════
# COURSE OVERVIEW PAGE
# ════════════════════════════════════════════════════════════════════════════

if page == "📚 Course Overview":
    overview.render()


# ════════════════════════════════════════════════════════════════════════════
# STUDENT SUBMIT PAGE
# ════════════════════════════════════════════════════════════════════════════

elif page == "📤 Submit Project":
    st.title("Submit Your ML Project")
    st.write("Upload your project file below. Accepted formats: PDF, Word (.docx), PowerPoint (.pptx)")

    with st.form("submit_form", clear_on_submit=True):
        team_name = st.text_input("Team Name *", placeholder="e.g. Team Alpha")

        project_options = {f"Project {n}: {PROJECTS[n]['name']}": n for n in PROJECTS}
        selected_label = st.selectbox("Select Project *", list(project_options.keys()))
        project_number = project_options[selected_label]

        uploaded_file = st.file_uploader(
            "Upload Project File *",
            type=["pdf", "docx", "pptx"],
            help="Max 200 MB"
        )

        submitted = st.form_submit_button("Submit Project", type="primary", use_container_width=True)

    if submitted:
        if not team_name.strip():
            st.error("Please enter your team name.")
        elif uploaded_file is None:
            st.error("Please upload a file.")
        else:
            safe_team = "".join(c for c in team_name.strip() if c.isalnum() or c in " _-").strip()
            anon_id = generate_anon_id(safe_team, project_number)

            dest_dir = SUBMISSIONS_DIR / f"project_{project_number}" / safe_team
            dest_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = dest_dir / filename

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            sub_id = db.add_submission(safe_team, project_number,
                                       uploaded_file.name, str(file_path), anon_id)
            audit.log_event(sub_id, anon_id, "submitted",
                            notes=f"file={uploaded_file.name}")

            st.success(f"Submitted successfully! Team: **{safe_team}** | {selected_label}")
            st.balloons()

    st.divider()
    st.caption("Need to review project requirements? Use the **Course Overview** page in the sidebar.")


# ════════════════════════════════════════════════════════════════════════════
# INSTRUCTOR DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

elif page == "📊 Instructor Dashboard":
    st.title("Instructor Dashboard")

    submissions = db.get_all_submissions()

    # ── Metrics ──────────────────────────────────────────────────────────────
    total    = len(submissions)
    pending  = sum(1 for s in submissions if s["status"] == "pending")
    ai_graded = sum(1 for s in submissions if s["status"] == "ai_graded")
    approved = sum(1 for s in submissions if s["status"] == "approved")
    pii_flagged = sum(1 for s in submissions if s.get("pii_detected"))

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", total)
    c2.metric("Pending", pending)
    c3.metric("AI Drafted", ai_graded)
    c4.metric("Approved", approved)
    c5.metric("PII Flagged", pii_flagged, delta="review" if pii_flagged else None,
              delta_color="inverse")

    st.divider()

    # ── Grade All Pending ────────────────────────────────────────────────────
    col_btn, col_filter = st.columns([1, 2])

    with col_btn:
        if pending > 0:
            if st.button(f"Grade All Pending ({pending})", type="primary"):
                pending_subs = [s for s in submissions if s["status"] == "pending"]
                progress_bar = st.progress(0, text="Starting...")
                for i, sub in enumerate(pending_subs):
                    progress_bar.progress(
                        i / len(pending_subs),
                        text=f"Grading {sub.get('anon_id', sub['team_name'])} — Project {sub['project_number']}..."
                    )
                    try:
                        text    = extractor.extract_text(sub["file_path"])
                        anon_id = sub.get("anon_id") or generate_anon_id(sub["team_name"], sub["project_number"])
                        result  = grader.grade_submission(
                            sub["project_number"], text, sub["team_name"], anon_id
                        )
                        db.save_ai_grade(
                            sub["id"],
                            result["grade"], result["feedback"],
                            criterion_scores  = result["criterion_scores"],
                            syllabus_score    = result["syllabus_score"],
                            syllabus_met      = result["syllabus_met"],
                            syllabus_missing  = result["syllabus_missing"],
                            pii_detected      = result["pii_detected"],
                            pii_types         = result["pii_types"],
                        )
                        audit.log_event(
                            sub["id"], anon_id, "graded",
                            model_used     = result["model_used"],
                            input_chars    = result["input_chars"],
                            output_chars   = result["output_chars"],
                            ai_grade       = result["grade"],
                            pii_detected   = result["pii_detected"],
                            pii_types      = result["pii_types"],
                            syllabus_score = result["syllabus_score"],
                        )
                    except Exception as e:
                        anon_id = sub.get("anon_id", "ANON-ERR")
                        db.save_ai_grade(sub["id"], "ERROR", f"Could not grade: {e}")
                        audit.log_event(sub["id"], anon_id, "graded",
                                        ai_grade="ERROR", notes=str(e))
                progress_bar.progress(1.0, text="Done!")
                st.rerun()

    with col_filter:
        filter_options = ["All Projects"] + [f"Project {n}" for n in PROJECTS]
        filter_choice = st.selectbox("Filter by project", filter_options)

    # ── Submission list ───────────────────────────────────────────────────────
    if filter_choice != "All Projects":
        proj_num = int(filter_choice.split()[-1])
        submissions = [s for s in submissions if s["project_number"] == proj_num]

    if not submissions:
        st.info("No submissions yet.")

    for sub in submissions:
        status_icon   = STATUS_COLORS.get(sub["status"], "⚪")
        grade_display = sub["final_grade"] or sub["ai_grade"] or "—"
        syllabus_pct  = sub.get("syllabus_score") or 0
        pii_warn      = " ⚠️ PII" if sub.get("pii_detected") else ""
        label = (
            f"{status_icon} **{sub['team_name']}** — "
            f"Project {sub['project_number']} — "
            f"{sub['submitted_at']} — "
            f"Grade: {grade_display} — "
            f"Syllabus: {syllabus_pct}%{pii_warn}"
        )

        with st.expander(label, expanded=(sub["status"] == "ai_graded")):

            # ── Top row: info + actions ───────────────────────────────────────
            col_info, col_actions = st.columns([3, 1])

            with col_info:
                st.write(f"**File:** {sub['filename']}")
                st.write(f"**Status:** {sub['status'].replace('_', ' ').title()}")
                st.caption(f"Anon ID: `{sub.get('anon_id', 'not set')}`")
                if sub.get("pii_detected"):
                    types_str = ", ".join(json.loads(sub.get("pii_types") or "[]"))
                    st.warning(f"PII detected in submission ({types_str}). Redacted before AI processing.")
                if sub.get("approved_at"):
                    st.write(f"**Approved:** {sub['approved_at']}")

            with col_actions:
                file_path = Path(sub["file_path"])
                if file_path.exists():
                    if st.button("Open / Present", key=f"open_{sub['id']}"):
                        subprocess.run(["open", str(file_path)])
                else:
                    st.warning("File not found")

            # ── Single-submission Grade with AI ───────────────────────────────
            if sub["status"] == "pending":
                if st.button("Grade with AI", key=f"grade_{sub['id']}"):
                    with st.spinner("Grading..."):
                        try:
                            text    = extractor.extract_text(sub["file_path"])
                            anon_id = sub.get("anon_id") or generate_anon_id(sub["team_name"], sub["project_number"])
                            result  = grader.grade_submission(
                                sub["project_number"], text, sub["team_name"], anon_id
                            )
                            db.save_ai_grade(
                                sub["id"],
                                result["grade"], result["feedback"],
                                criterion_scores  = result["criterion_scores"],
                                syllabus_score    = result["syllabus_score"],
                                syllabus_met      = result["syllabus_met"],
                                syllabus_missing  = result["syllabus_missing"],
                                pii_detected      = result["pii_detected"],
                                pii_types         = result["pii_types"],
                            )
                            audit.log_event(
                                sub["id"], anon_id, "graded",
                                model_used     = result["model_used"],
                                input_chars    = result["input_chars"],
                                output_chars   = result["output_chars"],
                                ai_grade       = result["grade"],
                                pii_detected   = result["pii_detected"],
                                pii_types      = result["pii_types"],
                                syllabus_score = result["syllabus_score"],
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            # ── XAI, Syllabus, Audit panels (shown once AI has graded) ────────
            if sub["status"] in ("ai_graded", "approved"):
                raw_scores  = sub.get("criterion_scores") or "{}"
                raw_met     = sub.get("syllabus_met") or "[]"
                raw_missing = sub.get("syllabus_missing") or "[]"

                try:
                    criterion_scores = json.loads(raw_scores)
                except json.JSONDecodeError:
                    criterion_scores = {}
                try:
                    syllabus_met     = json.loads(raw_met)
                    syllabus_missing = json.loads(raw_missing)
                except json.JSONDecodeError:
                    syllabus_met = syllabus_missing = []

                # XAI Criterion Breakdown
                if criterion_scores:
                    with st.expander("XAI — Criterion-by-Criterion Scores", expanded=False):
                        import pandas as pd
                        xai_rows = []
                        total_scored = 0
                        total_max = 0
                        for crit, vals in criterion_scores.items():
                            score = vals.get("score", 0)
                            max_  = vals.get("max", 0)
                            total_scored += score
                            total_max    += max_
                            pct = round(score / max_ * 100) if max_ else 0
                            xai_rows.append({
                                "Criterion":     crit,
                                "Score":         score,
                                "Max":           max_,
                                "Pct":           f"{pct}%",
                                "Justification": vals.get("justification", ""),
                            })
                        if xai_rows:
                            st.dataframe(pd.DataFrame(xai_rows), use_container_width=True, hide_index=True)
                            if total_max:
                                st.caption(f"Total: {total_scored} / {total_max} ({round(total_scored/total_max*100)}%)")

                # Syllabus Alignment
                with st.expander(f"Syllabus Alignment — {syllabus_pct}% match with AIML-501 outcomes", expanded=False):
                    if syllabus_met:
                        st.markdown("**Outcomes addressed:**")
                        for o in syllabus_met:
                            st.markdown(f"- {o}")
                    if syllabus_missing:
                        st.markdown("**Outcomes not clearly addressed:**")
                        for o in syllabus_missing:
                            st.markdown(f"- {o}")
                    if not syllabus_met and not syllabus_missing:
                        st.write("No alignment data yet.")

                # RAI Audit Trail
                with st.expander("RAI Audit Trail", expanded=False):
                    trail = audit.get_audit_trail(sub["id"])
                    if trail:
                        import pandas as pd
                        trail_rows = []
                        for entry in trail:
                            pii_types_list = json.loads(entry.get("pii_types") or "[]")
                            trail_rows.append({
                                "Timestamp":       entry["timestamp"],
                                "Event":           entry["event_type"].title(),
                                "Anon ID":         entry["anon_id"],
                                "Model":           entry.get("model_used") or "—",
                                "Input chars":     entry.get("input_chars") or "—",
                                "AI Grade":        entry.get("ai_grade") or "—",
                                "PII Detected":    "Yes" if entry.get("pii_detected") else "No",
                                "PII Types":       ", ".join(pii_types_list) or "—",
                                "Syllabus Score":  entry.get("syllabus_score") or "—",
                                "Human Modified":  "Yes" if entry.get("human_modified") else "—",
                                "Final Grade":     entry.get("final_grade") or "—",
                            })
                        st.dataframe(pd.DataFrame(trail_rows), use_container_width=True, hide_index=True)
                    else:
                        st.write("No audit entries yet.")

                # Approve / Edit Grade
                with st.form(key=f"approve_form_{sub['id']}"):
                    st.markdown("**AI Feedback (read-only):**")
                    st.text_area(
                        "AI Feedback",
                        value=sub.get("ai_feedback") or "",
                        height=200,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    st.markdown("**Edit before posting:**")
                    final_grade = st.text_input(
                        "Final Grade",
                        value=sub.get("final_grade") or sub.get("ai_grade") or "",
                        key=f"fg_{sub['id']}"
                    )
                    final_feedback = st.text_area(
                        "Final Feedback (posted to student)",
                        value=sub.get("final_feedback") or sub.get("ai_feedback") or "",
                        height=250,
                        key=f"ff_{sub['id']}"
                    )
                    approve_btn = st.form_submit_button(
                        "Approve & Post Grade",
                        type="primary",
                        use_container_width=True
                    )
                    if approve_btn:
                        human_modified = (
                            final_grade.strip() != (sub.get("ai_grade") or "").strip()
                            or final_feedback.strip() != (sub.get("ai_feedback") or "").strip()
                        )
                        db.approve_grade(sub["id"], final_grade, final_feedback)
                        anon_id = sub.get("anon_id", "ANON-?")
                        audit.log_event(
                            sub["id"], anon_id, "approved",
                            human_modified = human_modified,
                            final_grade    = final_grade,
                            ai_grade       = sub.get("ai_grade"),
                            notes          = "human edited" if human_modified else "accepted AI grade",
                        )
                        st.success("Grade posted!")
                        st.rerun()

    # ── Grades Summary Table ──────────────────────────────────────────────────
    st.divider()
    st.subheader("Grades Summary")
    approved_subs = [s for s in db.get_all_submissions() if s["status"] == "approved"]
    if approved_subs:
        import pandas as pd
        rows = []
        for s in approved_subs:
            rows.append({
                "Team":           s["team_name"],
                "Anon ID":        s.get("anon_id") or "—",
                "Project":        f"Project {s['project_number']}",
                "Grade":          s["final_grade"],
                "Syllabus Match": f"{s.get('syllabus_score') or 0}%",
                "PII":            "Yes" if s.get("pii_detected") else "No",
                "Submitted":      s["submitted_at"],
                "Approved":       s["approved_at"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Full RAI Audit Log tab ────────────────────────────────────────────────
    st.divider()
    with st.expander("Full RAI Audit Log", expanded=False):
        all_logs = audit.get_all_audit_logs()
        if all_logs:
            import pandas as pd
            st.dataframe(pd.DataFrame(all_logs), use_container_width=True, hide_index=True)
        else:
            st.write("No audit records yet.")
