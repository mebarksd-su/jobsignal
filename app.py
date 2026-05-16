# =========================
# IMPORTS
# =========================
import streamlit as st
import pandas as pd
from datetime import date
from urllib.parse import urlparse, unquote
import re
import os
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
from utils.resume_parser import extract_resume_text
from utils.section_parser import (
    extract_skills_section
)
from utils.signal_strength import calculate_signal_strength











def clean_url_words(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())

    ignored_words = {
        "job",
        "jobs",
        "careers",
        "career",
        "apply",
        "application",
        "posting",
        "details",
        "view",
        "req",
        "requisition",
        "opportunity",
        "opportunities",
        "search",
        "description",
        "external",
        "en",
        "us",
        "usa",
        "remote",
        "hybrid",
        "onsite",
        "on",
        "site",
        "student",
        "students",
        # "internship",
        # "intern",
        "fulltime",
        "full",
        "time"
    }

    return [
        word for word in words
        if word not in ignored_words and len(word) > 2
    ]



def format_guess(text):
    return text.replace("-", " ").replace("_", " ").strip().title()



def infer_application_details_from_link(job_link):
    parsed = urlparse(job_link)
    domain = parsed.netloc.lower().replace("www.", "")
    path = unquote(parsed.path.lower())
    query = unquote(parsed.query.lower())

    company_guess = ""
    role_guess = ""
    notes = []

    domain_parts = [part for part in domain.split(".") if part]
    path_parts = [part for part in path.split("/") if part]

    # -------------------------
    # GREENHOUSE
    # Common format: boards.greenhouse.io/company/jobs/12345
    # -------------------------

    if "greenhouse" in domain:
        if len(path_parts) > 0:
            company_guess = format_guess(path_parts[0])
        notes.append("Detected Greenhouse job link.")

    # -------------------------
    # LEVER
    # Common format: jobs.lever.co/company/job-id
    # -------------------------

    elif "lever.co" in domain:
        if len(path_parts) > 0:
            company_guess = format_guess(path_parts[0])
        notes.append("Detected Lever job link.")

    # -------------------------
    # WORKDAY
    # Common format often uses company subdomain or path title slugs.
    # -------------------------

    elif "workdayjobs" in domain or "myworkdayjobs" in domain:
        if len(domain_parts) > 0:
            company_guess = format_guess(domain_parts[0])
        notes.append("Detected Workday job link.")

    # -------------------------
    # LINKEDIN
    # LinkedIn URLs often hide company data, so role guessing is limited.
    # -------------------------

    elif "linkedin" in domain:
        notes.append("Detected LinkedIn job link. Company auto-fill may be limited from the URL alone.")

    # -------------------------
    # HANDSHAKE
    # Handshake often hides useful details behind login/session routing.
    # -------------------------

    elif "handshake" in domain:
        notes.append("Detected Handshake job link. Job details may need to be entered manually.")

    # -------------------------
    # INDEED
    # Indeed often uses IDs and query parameters instead of readable titles.
    # -------------------------

    elif "indeed" in domain:
        notes.append("Detected Indeed job link. Job details may need to be entered manually.")

    # -------------------------
    # GENERIC COMPANY / CAREERS SITE
    # Uses the domain as a company guess when it is not a known job board.
    # -------------------------

    else:
        platform_words = {
            "jobs",
            "careers",
            "boards",
            "apply",
            "recruiting",
            "talent"
        }

        if len(domain_parts) > 0:
            first_domain_part = domain_parts[0]

            if first_domain_part in ["careers", "jobs"] and len(domain_parts) > 1:
                company_guess = format_guess(domain_parts[1])
            elif first_domain_part not in platform_words:
                company_guess = format_guess(first_domain_part)

    # -------------------------
    # ROLE GUESSING
    # Pulls readable role words from the URL path and query string.
    # -------------------------

    combined_text = f"{path} {query}"
    role_words = clean_url_words(combined_text)

    if company_guess:
        company_words = company_guess.lower().split()
        role_words = [
            word for word in role_words
            if word not in company_words
        ]

    if len(role_words) >= 2:
        role_guess = " ".join(role_words[-7:]).title()

    return {
        "company": company_guess,
        "role": role_guess,
        "notes": notes
    }



# =========================
# PAGE CONFIGURATION + NAVIGATION
# =========================

st.set_page_config(page_title="RoleRadar", layout="wide")

page = st.sidebar.radio(
    "Navigation",
    [
        "Command Center",
        "Radar Lab",
        "Help"
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

st.title("RoleRadar")
st.caption("Career intelligence for modern applicants.")

# =========================
# DEMO LOGIN GATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")
    st.write("Use one of the demo accounts to access RoleRadar.")

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

    st.info("Demo accounts: malachi / roleradar, demo / demo123, recruiter / recruiter123")
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
# HELP PAGE
# Explains the major RoleRadar tools in plain language.
# This page also helps demo viewers understand what the app can do.
# =========================

if page == "Help":
    st.header("RoleRadar Guide")
    st.write(
        "Use this page as a quick guide to RoleRadar's main tools, scores, and workflow."
    )

    st.subheader("Command Center")
    st.write(
        "Track job applications, statuses, notes, links, follow-up activity, and application trends in one place."
    )

    st.subheader("Smart Application Intake")
    st.write(
        "Paste a job link and RoleRadar will try to auto-fill the company name and job title. "
        "Some platforms hide job details behind IDs, redirects, or login pages, so users should always review the fields before saving."
    )

    st.subheader("Radar Lab")
    st.write(
        "Upload a resume PDF and paste a job description to compare your resume against a specific role. "
        "RoleRadar checks skill overlap, wording alignment, priority gaps, and improvement steps."
    )

    st.subheader("RadarScore")
    st.write(
        "RadarScore combines skill match and resume alignment into one overall role-fit score. "
        "It is a decision-support score, not a hiring prediction."
    )

    st.subheader("Radar Strength")
    st.write(
        "Radar Strength measures how reliable the analysis is based on resume structure and detected evidence. "
        "A clear skills section and strong detected evidence increase this score."
    )

    st.subheader("Priority Skill Analysis")
    st.write(
        "Priority Skill Analysis highlights the most important missing skills for the detected role type. "
        "This helps users focus on the gaps that matter most instead of treating every missing keyword equally."
    )

    st.subheader("Resume Action Plan")
    st.write(
        "The Resume Action Plan turns missing skills and weak alignment areas into practical next steps, "
        "including resume edits, small projects, and skill-building resources."
    )

    st.subheader("Follow-Up Generator")
    st.write(
        "The Follow-Up Generator creates draft messages based on saved applications, including post-application follow-ups, "
        "interview thank-you notes, and recruiter networking messages."
    )

    st.subheader("Current MVP Limitations")
    st.write(
        "RoleRadar currently uses structured parsing, scoring logic, and template-based guidance. "
        "Future versions can add deeper AI extraction, stronger job-link parsing, and smarter resume rewriting."
    )

    st.stop()


# =========================
# APPLICATION TRACKER PAGE
# Main dashboard for tracking, editing, filtering, and analyzing applications.
# =========================

if page == "Command Center":
    st.write("Track applications, monitor progress, and turn job search activity into career intelligence.")

    # -------------------------
    # ADD NEW APPLICATION FORM
    # Kept inside an expander so the dashboard stays first and the form does not dominate the page.
    # -------------------------

    with st.expander(
            "Add New Application",
            expanded=st.session_state.get("add_app_expanded", False)
    ):

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

        job_link = st.text_input("Job Link", key="job_link")

        auto_fill_button = st.button("Try Auto-Fill from Job Link")

        if auto_fill_button:
            if st.session_state.job_link.strip() == "":
                st.warning("Paste a job link first, then try auto-fill.")
            else:
                inferred_details = infer_application_details_from_link(
                    st.session_state.job_link
                )

                parser_notes = inferred_details.get("notes", [])

                st.session_state.company = ""
                st.session_state.role = ""

                if inferred_details["company"]:
                    st.session_state.company = inferred_details["company"]

                if inferred_details["role"]:
                    st.session_state.role = inferred_details["role"]

                if inferred_details["company"] or inferred_details["role"]:
                    st.success(
                        "RoleRadar filled what it could. Review the fields below, then click Add Application to save."
                    )

                    for note in parser_notes:
                        st.info(note)
                else:
                    st.info("RoleRadar could not confidently auto-fill this link yet. Add the details manually.")

                    for note in parser_notes:
                        st.info(note)

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
                st.session_state["add_app_expanded"] = False

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

    filtered_df = df.copy()

    # -------------------------
    # APPLICATION BREAKDOWN
    # Compact summary tables replace oversized bar charts for a cleaner tracker experience.
    # -------------------------

    st.header("Application Breakdown")

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.subheader("Status Breakdown")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Applications"]
        st.table(status_counts.style.hide(axis="index"))

        st.subheader("Work Arrangement")
        work_arrangement_counts = (
            df["Work Arrangement"]
            .fillna("Not Specified")
            .replace("", "Not Specified")
            .value_counts()
            .reset_index()
        )
        work_arrangement_counts.columns = ["Work Arrangement", "Applications"]
        st.table(work_arrangement_counts.style.hide(axis="index"))

    with breakdown_col2:
        st.subheader("Most Applied Companies")
        company_counts = df["Company"].value_counts().head(3).reset_index()
        company_counts.columns = ["Company", "Applications"]
        st.table(company_counts.style.hide(axis="index"))

        st.subheader("Most Applied Locations")
        location_counts = (
            df["Location"]
            .replace("", "Unknown")
            .fillna("Unknown")
            .value_counts()
            .head(3)
            .reset_index()
        )
        location_counts.columns = ["Location", "Applications"]
        st.table(location_counts.style.hide(axis="index"))

    # -------------------------
    # EXPORT DATA
    # -------------------------

    st.header("Export Data")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Applications CSV",
        data=csv_data,
        file_name="roleradar_applications.csv",
        mime="text/csv"
    )

    # -------------------------
    # RECENT APPLICATIONS
    # -------------------------

    st.subheader("Recent Applications")
    recent_df = df.tail(5)

    st.dataframe(
        recent_df,
        width="stretch",
        hide_index=True
    )


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
    # APPLICATION ACTIVITY
    # Shows recent application activity by date.
    # A table is clearer than a timeline chart while the dataset is still small.
    # =========================

    st.header("Application Activity")

    timeline_df = df.copy()

    timeline_df["Date Added"] = pd.to_datetime(
        timeline_df["Date Added"]
    ).dt.date

    applications_over_time = (
        timeline_df.groupby("Date Added")
        .size()
        .reset_index(name="Applications Added")
        .sort_values(by="Date Added", ascending=False)
    )

    if len(applications_over_time) > 0:
        st.table(applications_over_time.head(7).style.hide(axis="index"))
    else:
        st.info("No application activity tracked yet.")

    # =========================
    # APPLICATION STRATEGY INSIGHTS
    # Uses the recommendation engine to generate strategic application advice.
    # =========================

    st.header("Application Strategy Insights")

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

    st.subheader("Strategic Insights")

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

    st.header("Manage Applications")

    st.subheader("Filter Applications")

    search_term = st.text_input(
        "Search Company or Job Title",
        key="manage_search"
    )

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Applied", "Interviewing", "Rejected", "Offer"],
        key="manage_status_filter"
    )

    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Company"].str.contains(search_term, case=False, na=False) |
            filtered_df["Role"].str.contains(search_term, case=False, na=False)
        ]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.write(f"Showing {len(filtered_df)} matching applications.")

    st.subheader("Application List")

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
# Resume analysis, job-fit scoring, and resume optimization tools.
# =========================

if page == "Radar Lab":

    st.caption("Upload a resume, paste a job description, and let RoleRadar evaluate skill match, alignment, priority gaps, and improvement steps.")

    # -------------------------
    # RESUME MATCH SCORING
    # Compares resume content against the target job description.
    # -------------------------

    st.header("Role Match Scanner")

    resume_text = ""
    skills_section_found = False

    uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
    )

    if uploaded_resume is not None:

        extracted_resume = extract_resume_text(
            uploaded_resume
        )

        skills_section = extract_skills_section(
            extracted_resume
        )

        if skills_section.strip() != "":
            resume_text = skills_section
            skills_section_found = True
            st.info("RoleRadar found and prioritized your resume skills section.")
        else:
            resume_text = extracted_resume
            skills_section_found = False
            st.warning(
                "RoleRadar could not find a clear skills section, so it analyzed the full resume instead."
            )

        st.success("Resume uploaded successfully.")

        with st.expander("Preview Extracted Resume Text"):

            st.text_area(
                "Full Extracted Resume Text",
                extracted_resume,
                height=300
            )


    match_job_description = st.text_area(
        "Paste Job Description for Match Score",
        height=200
    )

    match_button = st.button("Calculate Match Score")

    saved_analysis = load_latest_analysis()

    if match_button:
        if resume_text.strip() == "":
            st.error("Please upload a resume PDF before calculating a match score.")
            st.stop()

        if match_job_description.strip() == "":
            st.error("Please paste a job description before calculating a match score.")
            st.stop()

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
        signal_strength = calculate_signal_strength(
            matched_skills,
            missing_skills,
            skills_section_found,
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
            "signal_strength": signal_strength,
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
            "final_fit_score": final_fit_score,
            "signal_strength": signal_strength,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "smart_analysis": smart_analysis,
            "fit_analysis": fit_analysis,
            "action_plan": action_plan
        }

        st.subheader("Match Results")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("RadarScore", f"{final_fit_score}%")
        col4.metric("Radar Strength", f"{signal_strength['score']}%")
        col5.metric("Matched Skills", len(matched_skills))
        col6.metric("Missing Skills", len(missing_skills))

        st.info(f"Detected Role Type: {role_type}")
        st.info(
            f"Radar Strength: {signal_strength['label']} — {signal_strength['summary']}"
        )

        st.subheader("Priority Skill Analysis")

        col6, col7 = st.columns(2)
        col6.metric(
            "Priority Skills Matched",
            len(critical_matched)
        )
        col7.metric(
            "Priority Skills Missing",
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
        
        
        st.subheader("Radar Insights")
        for insight in smart_analysis:
            st.info(insight)

        st.subheader("Fit Summary")
        st.info(f"Radar Status: {fit_analysis['label']}")
        st.write(f"Summary: {fit_analysis['summary']}")
        st.write(f"Effort Needed: {fit_analysis['effort_level']}")
        st.write(f"Recommended Next Step: {fit_analysis['next_action']}")

        
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

        st.subheader("Overall Recommendation")

        if final_fit_score >= 80:
            st.success("Strong alignment. This resume appears well matched to the role.")
        elif final_fit_score >= 50:
            st.warning("Moderate alignment. Strengthen the resume language before applying.")
        else:
            st.error("Needs more role evidence. This resume may need clearer role-specific skills before applying.")

    elif saved_analysis:

        match_score = saved_analysis["match_score"]
        semantic_score = saved_analysis["semantic_score"]
        final_fit_score = saved_analysis.get("final_fit_score", match_score)
        signal_strength = saved_analysis.get(
            "signal_strength",
            {
                "label": "Not Available",
                "score": 0,
                "summary": "Signal Strength was not saved for this older analysis."
            }
        )
        matched_skills = saved_analysis["matched_skills"]
        missing_skills = saved_analysis["missing_skills"]
        smart_analysis = saved_analysis["smart_analysis"]
        fit_analysis = saved_analysis["fit_analysis"]
        action_plan = saved_analysis["action_plan"]

        st.subheader("Latest Saved Match Results")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("RadarScore", f"{final_fit_score}%")
        col4.metric("Radar Strength", f"{signal_strength['score']}%")
        col5.metric("Matched Skills", len(matched_skills))
        col6.metric("Missing Skills", len(missing_skills))

        st.info(
            f"Radar Strength: {signal_strength['label']} — {signal_strength['summary']}"
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

        st.subheader("Radar Insights")

        for insight in smart_analysis:
            st.info(insight)

        st.subheader("Fit Summary")

        st.info(f"Radar Status: {fit_analysis['label']}")
        st.write(f"Summary: {fit_analysis['summary']}")
        st.write(f"Effort Needed: {fit_analysis.get('effort_level', fit_analysis.get('tailoring_level', 'Not available'))}")
        st.write(f"Recommended Next Step: {fit_analysis['next_action']}")


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
    # ANALYSIS HISTORY VIEWER
    # Shows saved resume analysis history and score trends.
    # -------------------------

    st.header("Resume Analysis History")
    st.caption("Review previous resume analyses, score trends, and repeated skill gaps.")

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
        col2.metric("Latest RadarScore", f"{latest_score}%")
        col3.metric("Best RadarScore", f"{best_score}%")
        col4.metric("Average RadarScore", f"{average_score}%")

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
    # JOB DESCRIPTION ANALYZER
    # Detects skills and recommends resume focus areas.
    # -------------------------

    st.header("Job Description Radar")
    st.caption("Use this when you want to inspect a job description without running a full resume match.")

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
    # RESUME BULLET REWRITER
    # Strengthens resume bullets and improves role alignment.
    # -------------------------

    st.header("Rewrite a Resume Bullet")

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

        st.subheader("Resume Bullet Feedback")

        bullet_length = len(improved_bullet.split())

        if bullet_length < 10:
            st.warning("Your bullet is too short. Add measurable impact.")
        elif bullet_length > 35:
            st.warning("Your bullet may be too long. Keep it concise.")
        else:
            st.success("Bullet length looks strong for ATS readability.")

        if "%" not in improved_bullet and "increase" not in improved_bullet.lower():
            st.info("Consider adding measurable results, scope, or impact.")