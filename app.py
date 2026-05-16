# =========================
# IMPORTS
# =========================
import streamlit as st
import pandas as pd
from datetime import date

from pages.radar_lab_page import render_radar_lab_page
from utils.auth import login_user, logout_user
from utils.data_manager import load_applications, save_applications
from utils.analytics import add_analytics_columns
from utils.recommendation_engine import generate_recommendations
from utils.job_link_parser import infer_application_details_from_link










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
    render_radar_lab_page()

    