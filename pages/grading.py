import streamlit as st
from streamlit_option_menu import option_menu
from src import pdf_reader, llm_function, process_result, generate_eda
import pandas as pd
import json
import os

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/grading_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Session State Initialization ---
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = "Upload Rubric"
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "extracted_content" not in st.session_state:
    st.session_state["extracted_content"] = None
if "rubric_result" not in st.session_state:
    st.session_state["rubric_result"] = None
if "uploaded_student_files" not in st.session_state:
    st.session_state["uploaded_student_files"] = []

# --- Title ---
st.markdown("<div class='title'>Welcome to the Grading Hub 📝</div>", unsafe_allow_html=True)

# --- Main Menu ---
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
st.session_state["selected_option"] = selected_option  # Sync selected option with session state

# --- Upload Rubric Section ---
if st.session_state["selected_option"] == "Upload Rubric":
    st.markdown("<div class='h1'>Step 1: Upload PDF file containing Questions, Answers, and Grading Rubrics</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(" ", type="pdf", label_visibility="collapsed", key="pdf_uploader")

    if uploaded_file and (st.session_state["uploaded_file"] != uploaded_file):
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["extracted_content"] = pdf_reader.extract_pdf(uploaded_file)
        st.session_state["rubric_result"] = None  

    if st.session_state["extracted_content"] and st.session_state["rubric_result"] is None:
        extracted_text = st.session_state["extracted_content"]
        response = llm_function.extract_rubric(extracted_text)
        try:
            rubric_data = json.loads(response.strip("```json").strip())
            st.session_state["rubric_result"] = rubric_data
        except json.JSONDecodeError:
            st.error("Failed to parse the rubric result. Please check the extracted response.")
            st.write(response)

    if st.session_state["rubric_result"]:
        st.markdown("<div class='h2'>Questions and Rubrics</div>", unsafe_allow_html=True)
        for i, question_data in enumerate(st.session_state["rubric_result"], 1):
            with st.expander(f"Question {i}"):
                st.json({
                    "Question": question_data.get("question", "N/A"),
                    "Key Elements": question_data.get("key_elements", []),
                    "Rubric": question_data.get("rubric", {})
                })

# --- Grade Answer Section ---
if st.session_state["selected_option"] == "Grade Answer":
    st.markdown("<div class='h1'>Step 2: Upload student answer PDF files (Multiple files allowed)</div>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        " ",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="student_answers_uploader"
    )

    if uploaded_files:
        st.session_state["uploaded_student_files"] = uploaded_files

    if st.session_state["uploaded_student_files"]:
        st.markdown("<br>", unsafe_allow_html=True)  
        if st.button("Grade", key="grade_button"):
            results_cot = []  

            for uploaded_file in st.session_state["uploaded_student_files"]:
                student_id = uploaded_file.name.replace(".pdf", "")
                content = pdf_reader.extract_pdf(uploaded_file)
                student_text = content if isinstance(content, str) else ""

                if st.session_state["rubric_result"]:
                    rubric_result = st.session_state["rubric_result"]
                    response_aligned = llm_function.extract_student_answers(student_text, rubric_result)

                    try:
                        aligned_answers = json.loads(response_aligned.strip("```json").strip())
                    except json.JSONDecodeError:
                        st.error("Failed to parse the aligned answers. Please check the response.")
                        st.write(response_aligned)
                        continue

                    for question_data, student_data in zip(rubric_result, aligned_answers):
                        response = llm_function.grade_student_answer(
                            question=question_data.get("question", ""),
                            key_elements=question_data.get("key_elements", []),
                            rubric=question_data.get("rubric", {}),
                            student_id=student_id,
                            student_answer=student_data.get("student_answer", "")
                        )

                        results_cot.append({
                            "Student ID": student_id,
                            "Question": question_data.get("question", ""),
                            "Student Answer": student_data.get("student_answer", ""),
                            "LLM_Response": response
                        })

            results_df = pd.DataFrame(results_cot)
            results_df = process_result.process(results_df)
            st.session_state["results_df"] = results_df

    if st.session_state.get("results_df") is not None:
        st.markdown("### Grading Results:")
        st.dataframe(st.session_state["results_df"])
        csv = st.session_state["results_df"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="grading_results.csv",
            mime="text/csv",
            key="download_button"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Histogram of Scores")
            generate_eda.histogram(st.session_state["results_df"])

        with col2:
            st.markdown("### Boxplot of Scores")
            generate_eda.boxplot(st.session_state["results_df"])



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