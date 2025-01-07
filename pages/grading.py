import streamlit as st
from streamlit_option_menu import option_menu
from src import loader, llm_function, process_result, generate_eda
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

st.markdown(
    f"""
    <div class="title-container">
        <img src="data:image/png;base64,{loader.load_image(img_path='assets/logo.trans.png')}" alt="Grady Logo">
        <div class="title">Grady - Grading Hub</div>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- Main Menu ---
selected_option = option_menu(
    None,
    ["Upload Rubric", "Grade Answer", "Visualization"],
    menu_icon=None,
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "5px",
            "background-color": "#f8f7fdbd",
            "border": "2px solid #616163",
            "width": "100%",
            "max-width": "1100px",
            "margin": "3 auto",
        },
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "3px",
            "padding": "5px",
            "color": "#2e2e2f",
            "cursor": "pointer",
            "transition": "background-color 0.3s ease",
        },
        "nav-link-selected": {
            "background-color": "#e0e0ff",
            "font-weight": "bold",
        },
    },
)
st.session_state["selected_option"] = selected_option  

# --- Upload Rubric Section ---
if st.session_state["selected_option"] == "Upload Rubric":
    st.markdown("<div class='h1'>Create Assessment</div>", unsafe_allow_html=True)

    if "assessment_name" not in st.session_state:
        st.session_state["assessment_name"] = ""

    assessment_name = st.text_input(
        "",
        label_visibility="collapsed",
        value=st.session_state["assessment_name"],
        placeholder="Enter the course code (e.g., WIA2001 DATABASE)"
    )
    st.markdown("")
  
    if assessment_name:
        st.session_state["assessment_name"] = assessment_name
        st.markdown("<div class='h1'>Upload PDF file containing Questions, Answers, and Grading Rubrics</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Please upload the file according to the format in the sample.", 
            type="pdf", 
            key="pdf_uploader")
        
        view_rubric = st.checkbox("View Sample Rubric File")
        if view_rubric:
            st.markdown(loader.display_pdf("assets/sample_rubric.pdf"), unsafe_allow_html=True)
        with st.spinner("Grady is extracting rubric..."):
            if uploaded_file and (st.session_state["uploaded_file"] != uploaded_file):
                st.session_state["uploaded_file"] = uploaded_file
                st.session_state["extracted_content"] = loader.extract_pdf(uploaded_file)
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
                st.markdown(f"#### Questions and Rubrics")
                for i, question_data in enumerate(st.session_state["rubric_result"], 1):
                    with st.expander(f"Question {i}"):
                        st.json({
                            "Question": question_data.get("question", "N/A"),
                            "Marks Allocation": question_data.get("marks_allocation", "N/A"),
                            "Key Elements": question_data.get("key_elements", []),
                            "Rubric": question_data.get("rubric", {})
                        })

# --- Grade Answer Section ---
if st.session_state["selected_option"] == "Grade Answer":
    if not st.session_state["rubric_result"]:
        st.warning("No grading rubrics available. Please upload the grading rubric first.")
    else:
        st.markdown("<div class='h1'>Upload Answer PDF files (Multiple Files Allowed)</div>", unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Please upload the file according to the format in the sample.",
            type="pdf",
            accept_multiple_files=True,
            key="student_answers_uploader"
        )
        view_answer = st.checkbox("View Sample Answer File")
        if view_answer:
            st.markdown(loader.display_pdf("assets/sample_answer.pdf"), unsafe_allow_html=True)
            
        if uploaded_files:
            st.session_state["uploaded_student_files"] = uploaded_files

        if st.session_state["uploaded_student_files"]:
            st.markdown("<br>", unsafe_allow_html=True)  
            if st.button("Grade", key="grade_button"):
                with st.spinner("Grady is grading..."):
                    results_cot = []  

                    for uploaded_file in st.session_state["uploaded_student_files"]:
                        student_id = uploaded_file.name.replace(".pdf", "")
                        content = loader.extract_pdf(uploaded_file)
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
                                    "Marks Allocation": question_data.get("marks_allocation", ""),
                                    "Rubric": question_data.get("rubric", ""),
                                    "Student Answer": student_data.get("student_answer", ""),
                                    "LLM_Response": response
                                })
                                
                results_df = pd.DataFrame(results_cot)
                results_df = process_result.process(results_df)
                st.session_state["results_df"] = results_df

        if st.session_state.get("results_df") is not None:
            results_df = st.session_state["results_df"]
            student_ids = results_df["Student ID"].unique()
            st.markdown("<div class='h1'>View Results", unsafe_allow_html=True)
            selected_student_id = st.selectbox("Select a Student ID:", student_ids)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            if selected_student_id:
                student_data = results_df[results_df["Student ID"] == selected_student_id]
                st.markdown(f"#### Results for Student ID: {selected_student_id}")
                process_result.display(student_data, selected_student_id)                      
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                if st.session_state.get("results_df") is not None:
                    csv = st.session_state["results_df"].to_csv(index=False).encode('utf-8')
                    download_file_name = f"{st.session_state['assessment_name']}_grading_results.csv" if st.session_state["assessment_name"] else "grading_results.csv"
                    
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name=download_file_name,
                        mime="text/csv",
                        key="download_button"
                    )

# --- Visualization Section ---
if st.session_state["selected_option"] == "Visualization":
    if st.session_state.get("results_df") is None:
        st.warning("No grading results available. Please complete the grading process first.")
    else:
        results_df = st.session_state["results_df"]
        st.markdown(f"<div class='h1'>Assessment: {st.session_state['assessment_name']} ({results_df['Total_Marks_Allocation'].mean()} Marks)</div>", unsafe_allow_html=True)
        st.markdown(f"#### Total Students Evaluated: {results_df.shape[0]}")
        metrics = generate_eda.calculate_metrics(results_df)  
        for i in range(0, len(metrics), 3):
            cols = st.columns(3)
            for col, (title, value) in zip(cols, metrics[i:i+3]):
                with col:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-title">{title}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
         
        generate_eda.scoretable(results_df)
        col1, col2 = st.columns(2)

        with col1:
            generate_eda.histogram(results_df)

        with col2:
            generate_eda.boxplot(results_df)
        generate_eda.areachart(results_df)
    


        
        