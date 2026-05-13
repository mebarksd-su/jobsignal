import streamlit as st


def login_user(username, password):

    if username == "malachi" and password == "jobsignal":
        return True

    return False


def logout_user():

    st.session_state.logged_in = False