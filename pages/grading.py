import streamlit as st
from streamlit_option_menu import option_menu
from src import pdf_reader, llm_function, process_result, generate_eda
import pandas as pd
import json
import os

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "../styles/grading_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='title'>Automated Grading System</div>", unsafe_allow_html=True)

# --- Main Menu ---
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = "Upload Rubric"

# Option Menu Rendering
selected_option = option_menu(
    None,
    ["Upload Rubric", "Grade Answer"],
    menu_icon=None,
    default_index=["Upload Rubric", "Grade Answer"].index(st.session_state["selected_option"]),
    orientation="horizontal",
    styles={
        "container": {"class": "option-menu-container"},
        "nav-link": {"class": "option-menu-link"},
        "nav-link-selected": {"class": "option-menu-link-selected"},
    },
    key="main_option_menu"  
    )

# Sync Menu with Session State
st.session_state["selected_option"] = selected_option

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
    st.session_state["extracted_content"] = None

if st.session_state["selected_option"] == "Upload Rubric":
    st.markdown("<div class='h1'>Step 1: Upload PDF file contains Question, Answer and Grading Rubrics</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", key="pdf_uploader")

    if uploaded_file is not None:
        if st.session_state["uploaded_file"] != uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
            st.session_state["extracted_content"] = pdf_reader.extract_pdf(uploaded_file)

    if st.session_state["extracted_content"]:
        extracted_text = st.session_state["extracted_content"] 
        if extracted_text and "rubric_result" not in st.session_state:
            response = llm_function.extract_rubric(extracted_text)
            try:
                rubric_data = json.loads(response.strip("```json").strip())
                st.session_state["rubric_result"] = rubric_data
            except json.JSONDecodeError:
                st.error("Failed to parse the rubric result. Please check the extracted response.")
                st.write(response)  

    if "rubric_result" in st.session_state:
        st.write(st.session_state["rubric_result"])


if st.session_state["selected_option"] == "Grade Answer":
    if "uploaded_student_files" not in st.session_state:
        st.session_state["uploaded_student_files"] = []

    uploaded_files = st.file_uploader(
        "Upload PDF files for student answers",
        type="pdf",
        accept_multiple_files=True,
        key="student_answers_uploader"
    )

    if uploaded_files:
        st.session_state["uploaded_student_files"] = uploaded_files

    if st.session_state["uploaded_student_files"]:
        file_names = [uploaded_file.name for uploaded_file in st.session_state["uploaded_student_files"]]

        if "rubric_result" in st.session_state:
            question = st.session_state["rubric_result"].get("question", "")
            key_elements = st.session_state["rubric_result"].get("key_elements", [])
            rubric = st.session_state["rubric_result"].get("rubric", {})

 
        if st.button("Grade", key="grade_button"):
            results_cot = []

            for uploaded_file in st.session_state["uploaded_student_files"]:
                student_id = uploaded_file.name.replace(".pdf", "")  
                content = pdf_reader.extract_pdf(uploaded_file)
                student_answer = content if isinstance(content, str) else ""

                if "rubric_result" in st.session_state:
                    response = llm_function.grade_student_answer(
                        question=question,
                        key_elements=key_elements,
                        rubric=rubric,
                        student_id=student_id,
                        student_answer=student_answer
                    )

                    results_cot.append({
                        "Student ID": student_id,
                        "Student Answer": student_answer,
                        "LLM_Response": response
                    })

            results_df = pd.DataFrame(results_cot)
            results_df = process_result.extract(results_df)
            results_df = results_df.drop(columns=['LLM_Response'])
            st.dataframe(results_df)
            generate_eda.visualization_report(results_df)
            

# Render content based on selected option
# if selected_option == "Info":
#     # --- Info Tab Content ---
#         col1, col2= st.columns([2, 2])

#         with col1:
#             institute = st.text_input("Institute", "(institute)")
#             department = st.text_input("Department", "(department)")
#             date = st.date_input("Date")
            
#         with col2:
#             course_code = st.text_input("Course Code", "(course title)")
#             course_title = st.text_input("Course Title", "(course title)")
            
#         # Grade Thresholds Table
#         st.write("Grade Thresholds")
#         data = {
#             "Grade": ["A", "B", "C", "D", "Fail"],
#             "Mark": [90, 80, 70, 50, 0],
#         }
#         df = pd.DataFrame(data)
#         edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

#         # Buttons for adding or removing rows
#         st.markdown(
#             """
#             <div style="display: flex; justify-content: space-between;">
#                 <button style="padding: 10px 20px; background-color: #f63366; border: none; color: white; cursor: pointer;">
#                     + Add row
#                 </button>
#                 <button style="padding: 10px 20px; background-color: #555; border: none; color: white; cursor: pointer;">
#                     - Remove row
#                 </button>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )