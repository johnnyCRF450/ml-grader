import streamlit as st
import os
import subprocess
from pathlib import Path
from datetime import datetime

import database as db
import extractor
import grader
import overview
from rubrics import PROJECTS

SUBMISSIONS_DIR = Path("data/submissions")
SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
db.init_db()

INSTRUCTOR_PIN = os.environ.get("GRADER_PIN", "1234")

STATUS_COLORS = {
    "pending":   "🔵",
    "ai_graded": "🟡",
    "approved":  "🟢",
}

st.set_page_config(page_title="ML Project Grader", layout="wide", page_icon="🎓")

# ── Sidebar navigation ──────────────────────────────────────────────────────

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
            dest_dir = SUBMISSIONS_DIR / f"project_{project_number}" / safe_team
            dest_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = dest_dir / filename

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            db.add_submission(safe_team, project_number, uploaded_file.name, str(file_path))

            st.success(f"✅ Submitted successfully! Team: **{safe_team}** | {selected_label}")
            st.balloons()

    st.divider()
    st.caption("Need to review the project requirements? Use the **Course Overview** page in the sidebar.")


# ════════════════════════════════════════════════════════════════════════════
# INSTRUCTOR DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

elif page == "📊 Instructor Dashboard":
    st.title("Instructor Dashboard")

    submissions = db.get_all_submissions()

    # ── Metrics ──
    total = len(submissions)
    pending = sum(1 for s in submissions if s["status"] == "pending")
    ai_graded = sum(1 for s in submissions if s["status"] == "ai_graded")
    approved = sum(1 for s in submissions if s["status"] == "approved")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Submissions", total)
    c2.metric("Pending", pending)
    c3.metric("AI Drafted", ai_graded)
    c4.metric("Approved", approved)

    st.divider()

    # ── Grade All Pending ──
    col_btn, col_filter = st.columns([1, 2])
    with col_btn:
        if pending > 0:
            if st.button(f"⚡ Grade All Pending ({pending})", type="primary"):
                progress_bar = st.progress(0, text="Starting...")
                pending_subs = [s for s in submissions if s["status"] == "pending"]
                for i, sub in enumerate(pending_subs):
                    progress_bar.progress(
                        (i) / len(pending_subs),
                        text=f"Grading {sub['team_name']} — Project {sub['project_number']}..."
                    )
                    try:
                        text = extractor.extract_text(sub["file_path"])
                        grade, feedback = grader.grade_submission(
                            sub["project_number"], text, sub["team_name"]
                        )
                        db.save_ai_grade(sub["id"], grade, feedback)
                    except Exception as e:
                        db.save_ai_grade(sub["id"], "ERROR", f"Could not grade: {e}")
                progress_bar.progress(1.0, text="Done!")
                st.rerun()

    with col_filter:
        filter_options = ["All Projects"] + [f"Project {n}" for n in PROJECTS]
        filter_choice = st.selectbox("Filter by project", filter_options)

    # ── Submissions Table ──
    if filter_choice != "All Projects":
        proj_num = int(filter_choice.split()[-1])
        submissions = [s for s in submissions if s["project_number"] == proj_num]

    if not submissions:
        st.info("No submissions yet.")
    else:
        for sub in submissions:
            status_icon = STATUS_COLORS.get(sub["status"], "⚪")
            grade_display = sub["final_grade"] or sub["ai_grade"] or "—"
            label = f"{status_icon} **{sub['team_name']}** — Project {sub['project_number']} — {sub['submitted_at']} — Grade: {grade_display}"

            with st.expander(label, expanded=(sub["status"] == "ai_graded")):
                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.write(f"**File:** {sub['filename']}")
                    st.write(f"**Status:** {sub['status'].replace('_', ' ').title()}")
                    if sub["approved_at"]:
                        st.write(f"**Approved:** {sub['approved_at']}")

                with col_actions:
                    file_path = Path(sub["file_path"])
                    if file_path.exists():
                        if st.button("🖥️ Open / Present", key=f"open_{sub['id']}"):
                            subprocess.run(["open", str(file_path)])
                    else:
                        st.warning("File not found")

                # ── Grade with AI ──
                if sub["status"] == "pending":
                    if st.button("🤖 Grade with AI", key=f"grade_{sub['id']}"):
                        with st.spinner("Grading..."):
                            try:
                                text = extractor.extract_text(sub["file_path"])
                                grade, feedback = grader.grade_submission(
                                    sub["project_number"], text, sub["team_name"]
                                )
                                db.save_ai_grade(sub["id"], grade, feedback)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")

                # ── Approve Grade ──
                if sub["status"] in ("ai_graded", "approved"):
                    with st.form(key=f"approve_form_{sub['id']}"):
                        st.markdown("**AI Feedback (read-only preview):**")
                        st.text_area(
                            "AI Feedback",
                            value=sub["ai_feedback"] or "",
                            height=200,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                        st.markdown("**Edit before posting:**")
                        final_grade = st.text_input(
                            "Final Grade",
                            value=sub["final_grade"] or sub["ai_grade"] or "",
                            key=f"fg_{sub['id']}"
                        )
                        final_feedback = st.text_area(
                            "Final Feedback (posted to student)",
                            value=sub["final_feedback"] or sub["ai_feedback"] or "",
                            height=250,
                            key=f"ff_{sub['id']}"
                        )
                        approve_btn = st.form_submit_button(
                            "✅ Approve & Post Grade",
                            type="primary",
                            use_container_width=True
                        )
                        if approve_btn:
                            db.approve_grade(sub["id"], final_grade, final_feedback)
                            st.success("Grade posted!")
                            st.rerun()

    # ── Grades Summary Table ──
    st.divider()
    st.subheader("Grades Summary")
    approved_subs = [s for s in db.get_all_submissions() if s["status"] == "approved"]
    if approved_subs:
        rows = []
        for s in approved_subs:
            rows.append({
                "Team": s["team_name"],
                "Project": f"Project {s['project_number']}",
                "Grade": s["final_grade"],
                "Submitted": s["submitted_at"],
                "Approved": s["approved_at"],
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.write("No approved grades yet.")
