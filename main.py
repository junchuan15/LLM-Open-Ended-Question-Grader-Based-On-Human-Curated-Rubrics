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

model_page = st.Page(
    page="pages/model_info.py",
    title="Model Info",
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
        "Overview": [home_page, model_page],
        "Get Started": [grading_page, user_manual_page],
    }
)
main.run()
