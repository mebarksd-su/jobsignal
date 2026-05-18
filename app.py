# =========================
# IMPORTS
# =========================
import streamlit as st
from views.command_center_page import render_command_center_page

from views.radar_lab_page import render_radar_lab_page
from utils.auth import login_user, logout_user
from utils.data_manager import load_applications
from utils.analytics import add_analytics_columns










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


if page == "Command Center":
    render_command_center_page(df)


# =========================
# AI ANALYZER PAGE
# Resume analysis, job-fit scoring, and resume optimization tools.
# =========================

if page == "Radar Lab":
    render_radar_lab_page()

    