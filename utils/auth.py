import streamlit as st


# =========================
# DEMO USER STORE
# Demo-only users for local development and portfolio testing.
# Production auth should eventually use hashed passwords and a real database.
# =========================

DEMO_USERS = {
    "malachi": {
        "password": "jobsignal",
        "name": "Malachi",
        "role": "Owner"
    },
    "demo": {
        "password": "demo123",
        "name": "Demo User",
        "role": "Guest"
    },
    "recruiter": {
        "password": "recruiter123",
        "name": "Recruiter Demo",
        "role": "Viewer"
    }
}


def login_user(username, password):

    username = username.strip().lower()

    if username in DEMO_USERS:
        if DEMO_USERS[username]["password"] == password:
            st.session_state["current_user"] = username
            st.session_state["current_user_name"] = DEMO_USERS[username]["name"]
            st.session_state["current_user_role"] = DEMO_USERS[username]["role"]
            return True

    return False


def logout_user():

    st.session_state.logged_in = False

    if "current_user" in st.session_state:
        del st.session_state["current_user"]

    if "current_user_name" in st.session_state:
        del st.session_state["current_user_name"]

    if "current_user_role" in st.session_state:
        del st.session_state["current_user_role"]