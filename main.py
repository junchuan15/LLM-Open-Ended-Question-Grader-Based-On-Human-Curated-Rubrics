import streamlit as st

# --- PAGE SETUP ---
home_page = st.Page(
    page= "pages/home.py",
    title= "Home",
    icon = ":material/home:",
    default = True,
)

user_manual_page = st.Page(
    page= "pages/user_manual.py",
    title= "User Manual",
    icon = ":material/menu_book:",
)

about_me_page = st.Page(
    page= "pages/about_me.py",
    title= "About ME",
    icon = ":material/account_circle:",
)

grading_page = st.Page(
    page= "pages/grading.py",
    title= "Grading Hub",
    icon = ":material/rubric:",
)

model_page = st.Page(
    page= "pages/model_info.py",
    title= "Model Info",
    icon = ":material/robot:",
)

# --- NAVIGATION SETUP ---
main = st.navigation(
    {
        "Overview" : [home_page,user_manual_page,about_me_page],
        "Get Started" : [grading_page,model_page]
    }
)

main.run()