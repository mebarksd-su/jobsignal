# =========================
# IMPORTS
# =========================
import streamlit as st
import pandas as pd
from datetime import date
import os
import matplotlib.pyplot as plt
from utils.auth import login_user, logout_user
from utils.data_manager import load_applications, save_applications
from utils.analytics import add_analytics_columns
from utils.ai_tools import (
    detect_skills,
    generate_resume_recommendations,
    calculate_match_score,
    enhance_resume_bullet,
    detect_enhancement_keywords
)
from utils.skills_engine import (
    extract_skills,
    calculate_skill_frequency
)
from utils.recommendation_engine import generate_recommendations
from utils.semantic_matcher import calculate_semantic_match
from utils.smart_gap_analyzer import generate_gap_analysis
from utils.fit_classifier import classify_job_fit
from utils.action_plan_engine import generate_action_plan
from utils.analysis_storage import (
    save_latest_analysis,
    load_latest_analysis,
    save_analysis_to_history,
    load_analysis_history
)
from utils.skill_trend_engine import analyze_skill_trends
from utils.score_engine import calculate_final_fit_score
from utils.role_classifier import classify_role_type
from utils.critical_skills import ROLE_CRITICAL_SKILLS
from utils.rewrite_templates import generate_resume_bullet














# =========================
# PAGE CONFIGURATION + NAVIGATION
# =========================

st.set_page_config(page_title="JobSignal", layout="wide")

page = st.sidebar.radio(
    "Navigation",
    [
        "Application Tracker",
        "AI Analyzer"
    ]
)

# =========================
# DATA LOADING + CLEANUP
# Loads saved application data from the data manager utility.
# =========================

df = load_applications()


# =========================
# DERIVED ANALYTICS COLUMNS
# Adds calculated fields used throughout analytics and dashboards.
# =========================

df = add_analytics_columns(df)


# =========================
# GLOBAL UI
# Shared UI elements used across the app.
# =========================

st.title("JobSignal")

# =========================
# DEMO LOGIN GATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")
    st.write("Use one of the demo accounts to access JobSignal.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Login successful.")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.info("Demo accounts: malachi / jobsignal, demo / demo123, recruiter / recruiter123")
    st.stop()

if "toast_message" in st.session_state:
    st.toast(st.session_state["toast_message"])
    del st.session_state["toast_message"]

if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]

if "current_user_name" in st.session_state:
    st.sidebar.write(f"Logged in as: {st.session_state['current_user_name']}")
    st.sidebar.caption(f"Role: {st.session_state['current_user_role']}")

if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()


# =========================
# APPLICATION TRACKER PAGE
# Main dashboard for tracking, editing, filtering, and analyzing applications.
# =========================

if page == "Application Tracker":
    st.write("AI-powered internship and job application tracker.")

    # -------------------------
    # ADD NEW APPLICATION FORM
    # -------------------------

    st.header("Add New Application")

    if "company" not in st.session_state:
        st.session_state.company = ""

    if "role" not in st.session_state:
        st.session_state.role = ""

    if "location" not in st.session_state:
        st.session_state.location = ""

    if "job_link" not in st.session_state:
        st.session_state.job_link = ""

    if "notes" not in st.session_state:
        st.session_state.notes = ""

    company = st.text_input("Company Name", key="company")
    role = st.text_input("Job Title", key="role")
    location = st.text_input("Location", key="location")

    work_arrangement = st.selectbox(
        "Work Arrangement",
        ["Not Specified", "Remote", "Hybrid", "On-site"]
    )

    status = st.selectbox(
        "Application Status",
        ["Applied", "Interviewing", "Rejected", "Offer"]
    )

    job_link = st.text_input("Job Link", key="job_link")
    notes = st.text_area("Notes", key="notes")

    submit_button = st.button("Add Application")

    if submit_button:
        if company.strip() == "" or role.strip() == "":
            st.error("Company name and job title are required.")
        else:
            new_application = {
                "Date Added": str(date.today()),
                "Company": company.strip(),
                "Role": role.strip(),
                "Location": location.strip(),
                "Work Arrangement": work_arrangement,
                "Status": status,
                "Job Link": job_link.strip(),
                "Notes": notes.strip()
            }

            df = pd.concat([df, pd.DataFrame([new_application])], ignore_index=True)
            save_applications(df)

            st.session_state["success_message"] = "Application saved successfully."

            del st.session_state["company"]
            del st.session_state["role"]
            del st.session_state["location"]
            del st.session_state["job_link"]
            del st.session_state["notes"]

            st.rerun()

    # -------------------------
    # DASHBOARD METRICS
    # -------------------------

    st.header("Dashboard")

    total_applications = len(df)
    applied_count = len(df[df["Status"] == "Applied"])
    interview_count = len(df[df["Status"] == "Interviewing"])
    offer_count = len(df[df["Status"] == "Offer"])

    conversion_rate = 0
    if total_applications > 0:
        conversion_rate = round((interview_count / total_applications) * 100, 1)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Applications", total_applications)
    col2.metric("Applied", applied_count)
    col3.metric("Interviews", interview_count)
    col4.metric("Offers", offer_count)
    col5.metric("Interview Rate", f"{conversion_rate}%")

    st.write(
        f"You have {total_applications} total applications, "
        f"{interview_count} interviews, and {offer_count} offers tracked."
    )

    # -------------------------
    # FILTERS
    # -------------------------

    st.header("Filters")

    search_term = st.text_input("Search Company or Job Title")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Applied", "Interviewing", "Rejected", "Offer"]
    )

    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Company"].str.contains(search_term, case=False, na=False) |
            filtered_df["Role"].str.contains(search_term, case=False, na=False)
        ]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    # -------------------------
    # VISUAL ANALYTICS
    # Charts showing application trends and distribution patterns.
    # -------------------------

    st.subheader("Applications by Status")
    status_counts = df["Status"].value_counts()
    st.bar_chart(status_counts)

    if len(status_counts) > 0:
        st.subheader("Application Distribution")
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            status_counts,
            labels=status_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

    st.subheader("Top Companies Applied To")
    company_counts = df["Company"].value_counts().head(5)
    st.bar_chart(company_counts)

    st.subheader("Applications by Location")
    location_counts = df["Location"].replace("", "Unknown").fillna("Unknown").value_counts()
    st.bar_chart(location_counts)

    st.subheader("Applications by Work Arrangement")
    work_arrangement_counts = df["Work Arrangement"].fillna("Not Specified").value_counts()
    st.bar_chart(work_arrangement_counts)

    # -------------------------
    # EXPORT DATA
    # -------------------------

    st.header("Export Data")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Applications CSV",
        data=csv_data,
        file_name="jobsignal_applications.csv",
        mime="text/csv"
    )

    # -------------------------
    # RECENT APPLICATIONS
    # -------------------------

    st.subheader("Recent Applications")
    recent_df = df.tail(5)

    st.dataframe(
        recent_df,
        width="stretch"
    )

    # -------------------------
    # SAVED APPLICATIONS + KEY INSIGHTS
    # Displays filtered applications alongside analytics summaries.
    # -------------------------

    st.header("Saved Applications")
    st.write(f"Showing {len(filtered_df)} applications.")

    if len(filtered_df) > 0:
        most_common_status = filtered_df["Status"].mode()[0]
        top_company = filtered_df["Company"].mode()[0]

        st.subheader("Key Insights")
        st.info(
            f"""
            • Most common application status: {most_common_status}

            • Company applied to most often: {top_company}

            • Total shown applications: {len(filtered_df)}

            • Average days since applying: {round(filtered_df['Days Since Applied'].mean(), 1)}
            """
        )
        st.subheader("Application Analytics")

        top_locations = (
            df.groupby("Location")["Status"]
            .apply(lambda x: (x == "Interviewing").sum())
            .sort_values(ascending=False)
        )

        top_companies = (
            df.groupby("Company")["Status"]
            .apply(lambda x: (x == "Interviewing").sum())
            .sort_values(ascending=False)
        )

        rejection_rate = round(
            (len(df[df["Status"] == "Rejected"]) / len(df)) * 100,
            1
        ) if len(df) > 0 else 0

        offer_rate = round(
            (len(df[df["Status"] == "Offer"]) / len(df)) * 100,
            1
        ) if len(df) > 0 else 0

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rejection Rate", f"{rejection_rate}%")

        with col2:
            st.metric("Offer Rate", f"{offer_rate}%")

        st.subheader("Top Interview Locations")

        st.bar_chart(top_locations)

        st.subheader("Top Interview Companies")

        st.bar_chart(top_companies)
    else:
        st.info("No applications match your current filters.")

    # =========================
    # AI FOLLOW-UP GENERATOR
    # Generates recruiter and follow-up templates from application data.
    # =========================

    st.header("AI Follow-Up Generator")

    if len(df) > 0:

        selected_application = st.selectbox(
            "Select Application",
            df.index,
            format_func=lambda x: f"{df.loc[x, 'Company']} - {df.loc[x, 'Role']}",
            key="followup_select"
        )

        followup_type = st.selectbox(
            "Follow-Up Type",
            [
                "Post-Application Follow-Up",
                "Interview Thank You",
                "Recruiter Networking Message"
            ]
        )

        generate_followup = st.button("Generate Follow-Up Message")

        if generate_followup:

            company = df.loc[selected_application, "Company"]
            role = df.loc[selected_application, "Role"]

            generated_message = ""

            if followup_type == "Post-Application Follow-Up":

                generated_message = f"""
    Hello {company} Hiring Team,

    I hope you are doing well. I recently applied for the {role} position and wanted to follow up regarding my application status.

    I remain very interested in the opportunity and would love the chance to contribute my skills and experience to your team.

    Thank you for your time and consideration. I look forward to hearing from you.

    Best,
    Your Name
    """

            elif followup_type == "Interview Thank You":

                generated_message = f"""
    Hello {company} Team,

    Thank you again for taking the time to speak with me regarding the {role} opportunity.

    I enjoyed learning more about the role and the company, and the conversation further increased my interest in joining your team.

    I appreciate your consideration and look forward to hearing about next steps.

    Best,
    Your Name
    """

            elif followup_type == "Recruiter Networking Message":

                generated_message = f"""
    Hello,

    I hope you are doing well. My name is [Your Name], and I am very interested in opportunities related to the {role} position at {company}.

    I would love to connect and learn more about potential opportunities within your organization.

    Thank you for your time, and I hope to stay connected.

    Best,
    Your Name
    """

            st.subheader("Generated Follow-Up Message")
            st.code(generated_message, language="markdown")
    

    # =========================
    # APPLICATION TIMELINE
    # Visualizes application activity across dates.
    # =========================

    st.header("Application Timeline")

    timeline_df = df.copy()

    timeline_df["Date Added"] = pd.to_datetime(
        timeline_df["Date Added"]
    )

    applications_over_time = (
        timeline_df.groupby("Date Added")
        .size()
        .reset_index(name="Applications")
    )

    applications_over_time = applications_over_time.sort_values(
        by="Date Added"
    )

    st.line_chart(
        applications_over_time.set_index("Date Added")
    )

    # =========================
    # AI APPLICATION INSIGHTS
    # Uses the recommendation engine to generate strategic application advice.
    # =========================

    st.header("AI Application Insights")

    rejection_rate = round(
        (len(df[df["Status"] == "Rejected"]) / total_applications) * 100,
        1
    ) if total_applications > 0 else 0

    offer_rate = round(
        (len(df[df["Status"] == "Offer"]) / total_applications) * 100,
        1
    ) if total_applications > 0 else 0

    insight_col1, insight_col2 = st.columns(2)

    insight_col1.metric("Rejection Rate", f"{rejection_rate}%")
    insight_col2.metric("Offer Rate", f"{offer_rate}%")

    st.subheader("AI Strategic Insights")

    recommendations = generate_recommendations(df)

    for recommendation in recommendations:
        recommendation_lower = recommendation.lower()

        if "strong" in recommendation_lower or "effective" in recommendation_lower:
            st.success(recommendation)
        elif "low" in recommendation_lower or "high rejection" in recommendation_lower:
            st.warning(recommendation)
        else:
            st.info(recommendation)



    # -------------------------
    # MANAGE APPLICATIONS
    # Inline editing tools for statuses, notes, and deletion.
    # -------------------------

    st.subheader("Manage Applications")

    header1, header2, header3, header4, header5, header6, header7, header8 = st.columns([2, 2, 2, 2, 2, 3, 1, 1])

    header1.write("**Company**")
    header2.write("**Role**")
    header3.write("**Current Status**")
    header4.write("**Location**")
    header5.write("**Update Status**")
    header6.write("**Notes**")
    header7.write("**Save**")
    header8.write("**Action**")

    for index, row in filtered_df.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 2, 2, 2, 2, 3, 1, 1])

        col1.write(row["Company"])
        col2.write(row["Role"])
        col3.write(row["Status"])

        col4.write(
            row["Location"] if pd.notna(row["Location"]) and row["Location"] != "" else "Not Specified"
        )

        status_options = ["Applied", "Interviewing", "Rejected", "Offer"]

        new_status = col5.selectbox(
            "Status",
            status_options,
            index=status_options.index(row["Status"]),
            key=f"status_update_{index}",
            label_visibility="collapsed"
        )

        updated_notes = col6.text_area(
            "Notes",
            value=row["Notes"] if pd.notna(row["Notes"]) else "",
            key=f"notes_{index}",
            label_visibility="collapsed"
        )

        if col7.button("Save", key=f"save_notes_{index}"):
            df.loc[index, "Notes"] = updated_notes
            save_applications(df)
            st.session_state["toast_message"] = f"Saved notes for {row['Company']}"
            st.rerun()

        if new_status != row["Status"]:
            df.loc[index, "Status"] = new_status
            save_applications(df)
            st.success(f"Updated {row['Company']} status to {new_status}.")
            st.rerun()

        if col8.button("Delete", key=f"delete_{index}"):
            df = df.drop(index=index)
            df = df.reset_index(drop=True)
            save_applications(df)
            st.success("Application deleted successfully.")
            st.rerun()

    # -------------------------
    # BULK DELETE APPLICATION
    # Dropdown-based removal tool for saved applications.
    # -------------------------

    st.header("Delete Application")

    if len(df) > 0:
        delete_index = st.selectbox(
            "Select Application to Delete",
            df.index,
            format_func=lambda x: f"{df.loc[x, 'Company']} - {df.loc[x, 'Role']}"
        )

        delete_button = st.button("Delete Selected Application")

        if delete_button:
            df = df.drop(index=delete_index)
            df = df.reset_index(drop=True)
            save_applications(df)
            st.success("Application deleted successfully.")
            st.rerun()
    else:
        st.info("No applications available to delete.")


# =========================
# AI ANALYZER PAGE
# Resume analysis, ATS scoring, and AI-powered optimization tools.
# =========================

if page == "AI Analyzer":

    # -------------------------
    # JOB DESCRIPTION ANALYZER
    # Detects skills and recommends resume focus areas.
    # -------------------------

    st.header("AI Job Description Analyzer")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    analyze_button = st.button("Analyze Job Description")

    if analyze_button:
        detected_skills = extract_skills(job_description)

        st.subheader("Detected Skills")

        if detected_skills:
            for item in detected_skills:
                st.write(
                    f"• {item['display_skill']} ({item['category']})"
                )
        else:
            st.write("No matching skills detected.")

        st.subheader("Skill Frequency Analysis")

        skill_frequency = calculate_skill_frequency(
            detected_skills
        )
        for skill, count in skill_frequency.items():
            st.write(f"• {skill}: {count}")    

        st.subheader("AI Summary")

        st.write(
            "This role appears focused on analytical, technical, and communication skills. "
            "Candidates should emphasize relevant technical projects, problem-solving ability, "
            "and real-world experience."
        )

        st.subheader("Recommended Resume Focus")

        resume_recommendations = generate_resume_recommendations(detected_skills)

        for recommendation in resume_recommendations:
            st.write(f"• {recommendation}")

    # -------------------------
    # ANALYSIS HISTORY VIEWER
    # Shows saved resume analysis history and score trends.
    # -------------------------

    st.header("Resume Analysis History")

    analysis_history = load_analysis_history()
    skill_trends = analyze_skill_trends(
        analysis_history
    )

    if len(analysis_history) > 0:

        total_analyses = len(analysis_history)

        match_scores = [
            record["analysis"].get(
                "final_fit_score",
                record["analysis"]["match_score"]
            )
            for record in analysis_history
        ]

        semantic_scores = [
            record["analysis"]["semantic_score"]
            for record in analysis_history
        ]

        latest_record = analysis_history[-1]
        latest_score = latest_record["analysis"].get(
            "final_fit_score",
            latest_record["analysis"]["match_score"]
        )
        best_score = max(match_scores)
        average_score = round(sum(match_scores) / len(match_scores), 1)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Saved Analyses", total_analyses)
        col2.metric("Latest Match Score", f"{latest_score}%")
        col3.metric("Best Match Score", f"{best_score}%")
        col4.metric("Average Match Score", f"{average_score}%")

        all_missing_skills = []

        st.subheader("Top Resume Strengths")

        if len(skill_trends["trending_strengths"]) > 0:

            for skill, count in skill_trends["trending_strengths"]:
                st.success(
                    f"{skill} appeared as a matched skill in {count} analyses."
                )
        
        st.subheader("Top Skill Gaps")

        if len(skill_trends["trending_missing"]) > 0:

            for skill, count in skill_trends["trending_missing"]:
                st.warning(
                    f"{skill} appeared as a missing skill in {count} analyses."
                )

        for record in analysis_history:
            all_missing_skills.extend(
                record["analysis"]["missing_skills"]
            )

        if len(all_missing_skills) > 0:
            missing_skill_counts = pd.Series(all_missing_skills).value_counts()

            st.subheader("Most Common Missing Skills")
            st.bar_chart(missing_skill_counts)

        st.subheader("Recent Analysis History")

        history_rows = []

        for record in analysis_history[-5:]:
            history_rows.append({
                "Timestamp": record["timestamp"],
                "Final Fit Score": record["analysis"].get(
                    "final_fit_score",
                    record["analysis"]["match_score"]
                ),
                "Semantic Score": record["analysis"]["semantic_score"],
                "Matched Skills": len(record["analysis"]["matched_skills"]),
                "Missing Skills": len(record["analysis"]["missing_skills"])
            })

        history_df = pd.DataFrame(history_rows)

        st.dataframe(
            history_df,
            width="stretch"
        )

    else:
        st.info("No resume analyses saved yet.")

    # -------------------------
    # RESUME MATCH SCORING
    # Compares resume content against job description keywords.
    # -------------------------

    st.header("Resume Match Scoring")

    resume_text = st.text_area(
        "Paste Resume or Skills",
        height=200
    )

    match_job_description = st.text_area(
        "Paste Job Description for Match Score",
        height=200
    )

    match_button = st.button("Calculate Match Score")

    saved_analysis = load_latest_analysis()

    if match_button:
        (
            match_score,
            matched_skills,
            missing_skills,
            critical_matched,
            critical_missing
        ) = calculate_match_score(

            resume_text,
            match_job_description
        )
        semantic_score = calculate_semantic_match(
            resume_text,
            match_job_description
        )

        role_type = classify_role_type(match_job_description)
        critical_skills = ROLE_CRITICAL_SKILLS.get(role_type, [])

        missing_critical_skills = []

        for skill in critical_skills:
            if skill.lower() not in [
                s.lower() for s in matched_skills
            ]:
                missing_critical_skills.append(skill)

        final_fit_score = calculate_final_fit_score(
            match_score,
            semantic_score
        )
        smart_analysis = generate_gap_analysis(
            matched_skills,
            missing_skills,
            semantic_score
        )
        fit_analysis = classify_job_fit(
            match_score,
            semantic_score,
            matched_skills,
            missing_skills
        )
        action_plan = generate_action_plan(
            fit_analysis,
            missing_skills,
            semantic_score
        )
        latest_analysis = {
            "match_score": match_score,
            "semantic_score": semantic_score,
            "role_type": role_type,
            "final_fit_score": final_fit_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "smart_analysis": smart_analysis,
            "fit_analysis": fit_analysis,
            "action_plan": action_plan
        }
        save_latest_analysis(latest_analysis)
        save_analysis_to_history(latest_analysis)

        st.session_state["latest_match_results"] = {
            "match_score": match_score,
            "semantic_score": semantic_score,
            "role_type": role_type,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "smart_analysis": smart_analysis,
            "fit_analysis": fit_analysis,
            "action_plan": action_plan
        }

        st.subheader("Match Results")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("JobSignal Score", f"{final_fit_score}%")
        col4.metric("Matched Skills", len(matched_skills))
        col5.metric("Missing Skills", len(missing_skills))

        st.info(f"Detected Role Type: {role_type}")

        st.subheader("Critical Skill Analysis")

        col6, col7 = st.columns(2)
        col6.metric(
            "Critical Skills Matched",
        len(critical_matched)
        )
        col7.metric(
            "Critical Skills Missing",
            len(critical_missing)
        )

        st.subheader("Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matching skills found.")

        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No missing skills detected.")

        # =========================
        # RESUME IMPROVEMENT SUGGESTIONS
        # Generates realistic resume bullet ideas
        # based on missing skills.
        # =========================

        st.subheader("Suggested Resume Bullets")

        if missing_skills:
            for skill in missing_skills:
                suggested_bullet = generate_resume_bullet(skill)
                st.success(
                    f"{skill}: {suggested_bullet}"
                )
        else:
            st.write("No resume improvement suggestions needed right now.")

        # =========================
        # PRIORITY SKILL GAPS
        # Highlights the most important missing skills for the detected role.
        # =========================

        st.subheader("Priority Skill Gaps")

        if critical_missing:
            for skill in critical_missing:
                st.error(
                    f"{skill}: This is a higher-priority gap for this type of role. "
                    "Consider adding a project, bullet, or experience that demonstrates this skill."
                )
        else:
            st.write("No priority skill gaps detected.")
        
        
        st.subheader("Smart Resume Gap Analysis")
        for insight in smart_analysis:
            st.info(insight)

        st.subheader("AI Fit Classification")
        st.info(f"Fit Category: {fit_analysis['label']}")
        st.write(f"Summary: {fit_analysis['summary']}")
        st.write(f"Tailoring Needed: {fit_analysis['tailoring_level']}")
        st.write(f"Recommended Action: {fit_analysis['next_action']}")

        
        st.subheader("Resume Action Plan")

        for item in action_plan:

            st.markdown(f"### {item['title']}")

            st.write("**Why This Matters**")
            st.write(item["why_it_matters"])

            st.write("**Suggested Improvement**")
            st.write(item["suggested_project"])

            st.write("**Skills You’ll Gain**")

            for skill in item["skills_gained"]:
                st.write(f"• {skill}")

            st.write("**Resources**")

            for resource in item["resources"]:
                st.markdown(
                    f"- [{resource['title']}]({resource['url']}) ({resource['type']})"
                )

            st.write(f"**Difficulty:** {item['difficulty']}")
            st.write(f"**Estimated Time:** {item['estimated_time']}")

            st.divider()

        st.subheader("Recommendation")

        if final_fit_score >= 80:
            st.success("Strong fit. This resume appears well aligned with the role.")
        elif final_fit_score >= 50:
            st.warning("Moderate fit. Tailor your resume before applying.")
        else:
            st.error("Weak fit. This resume needs stronger alignment before applying.")

    elif saved_analysis:

        match_score = saved_analysis["match_score"]
        semantic_score = saved_analysis["semantic_score"]
        final_fit_score = saved_analysis.get("final_fit_score", match_score)
        matched_skills = saved_analysis["matched_skills"]
        missing_skills = saved_analysis["missing_skills"]
        smart_analysis = saved_analysis["smart_analysis"]
        fit_analysis = saved_analysis["fit_analysis"]
        action_plan = saved_analysis["action_plan"]

        st.subheader("Latest Saved Match Results")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("JobSignal Score", f"{final_fit_score}%")
        col4.metric("Matched Skills", len(matched_skills))
        col5.metric("Missing Skills", len(missing_skills))

        st.subheader("Matched Skills")

        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matching skills found.")

        st.subheader("Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No missing skills detected.")

        st.subheader("Smart Resume Gap Analysis")

        for insight in smart_analysis:
            st.info(insight)

        st.subheader("AI Fit Classification")

        st.info(f"Fit Category: {fit_analysis['label']}")
        st.write(f"Summary: {fit_analysis['summary']}")
        st.write(f"Tailoring Needed: {fit_analysis['tailoring_level']}")
        st.write(f"Recommended Action: {fit_analysis['next_action']}")


        st.subheader("Resume Action Plan")

        for item in action_plan:

            st.markdown(f"### {item['title']}")

            st.write("**Why This Matters**")
            st.write(item["why_it_matters"])

            st.write("**Suggested Improvement**")
            st.write(item["suggested_project"])

            st.write("**Skills You’ll Gain**")

            for skill in item["skills_gained"]:
                st.write(f"• {skill}")

            st.write("**Resources**")

            for resource in item["resources"]:
                st.markdown(
                    f"- [{resource['title']}]({resource['url']}) ({resource['type']})"
                )

            st.write(f"**Difficulty:** {item['difficulty']}")
            st.write(f"**Estimated Time:** {item['estimated_time']}")

            st.divider()
    # -------------------------
    # RESUME BULLET ENHANCER
    # Strengthens weak resume bullets and improves ATS alignment.
    # -------------------------

    st.header("AI Resume Bullet Enhancer")

    original_bullet = st.text_area(
        "Paste Resume Bullet",
        height=150
    )

    target_job_description = st.text_area(
        "Paste Target Job Description",
        height=200
    )

    enhance_button = st.button("Enhance Resume Bullet")

    if enhance_button:
        improved_bullet = enhance_resume_bullet(original_bullet)
        keyword_matches = detect_enhancement_keywords(target_job_description)

        st.subheader("Enhanced Resume Bullet")
        st.success(improved_bullet)

        st.subheader("Suggested Keywords to Include")

        if keyword_matches:
            for keyword in keyword_matches:
                st.write(f"• {keyword}")
        else:
            st.write("No major keywords detected.")

        st.subheader("ATS Optimization Feedback")

        bullet_length = len(improved_bullet.split())

        if bullet_length < 10:
            st.warning("Your bullet is too short. Add measurable impact.")
        elif bullet_length > 35:
            st.warning("Your bullet may be too long. Keep it concise.")
        else:
            st.success("Bullet length looks strong for ATS readability.")

        if "%" not in improved_bullet and "increase" not in improved_bullet.lower():
            st.info("Consider adding measurable metrics or impact.")