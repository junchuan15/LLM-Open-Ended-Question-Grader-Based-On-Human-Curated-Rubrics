import streamlit as st

st.set_page_config(
    layout="wide",                     
    initial_sidebar_state="collapsed",  
)

# --- PAGE SETUP ---
home_page = st.Page(
    page="pages/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

project_page = st.Page(
    page="pages/project_info.py",
    title="Project Info",
    icon=":material/robot:",
)

grading_page = st.Page(
    page="pages/grading.py",
    title="Grading Hub",
    icon=":material/rubric:",
)

user_manual_page = st.Page(
    page="pages/user_manual.py",
    title="User Manual",
    icon=":material/menu_book:",
)
# --- NAVIGATION SETUP ---
main = st.navigation(
    {
        "Overview": [home_page, project_page],
        "Get Started": [grading_page, user_manual_page],
    }
)
main.run()
