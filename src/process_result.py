import json
import streamlit as st
import pandas as pd

def process_llm_response(response_text):
    matched_key_elements = 0
    score = None
    key_element_matches_formatted = ""
    explanation = ""  

    try:
        response_data = json.loads(response_text)
        key_element_matches = response_data.get("Key Element Matching", [])
        matched_key_elements = response_data.get("Total Matched Key Elements", 0)
        score = response_data.get("Score", None)
        explanation = response_data.get("Explanation", "")  

        key_element_matches_formatted = "\n".join(
            [f"- Key Element: {match['Key Element']}  Matching Answer: {match['Matching Answer']}" 
             for match in key_element_matches]
        )

    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response_text}")
        key_element_matches_formatted = "Error decoding JSON"

    return key_element_matches_formatted, matched_key_elements, score, explanation  

def organize_result(df):
    df["Question_Index"] = df.groupby("Student ID").cumcount() + 1
    df["Question_Label"] = "Q" + df["Question_Index"].astype(str)

    pivot_df = df.pivot(index="Student ID", columns="Question_Label", 
                                values=["Question", "Marks Allocation", "Rubric", "Student Answer", "Key Element Matching", "Score", "Explanation"])  

    pivot_df.columns = [f"{col[1]}_{col[0]}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    column_order = ["Student ID"]
    for index in sorted(set(df["Question_Label"])):
        column_order.extend([
            f"{index}_Question",
            f"{index}_Marks Allocation",
            f"{index}_Rubric",
            f"{index}_Student Answer",
            f"{index}_Key Element Matching",
            f"{index}_Explanation",  
            f"{index}_Score"
        ])
    pivot_df = pivot_df[column_order]
    marks_columns = [col for col in pivot_df.columns if "Marks Allocation" in col]
    pivot_df["Total_Marks_Allocation"] = pivot_df[marks_columns].sum(axis=1)
    score_columns = [col for col in pivot_df.columns if "Score" in col]
    pivot_df["Total_Score"] = pivot_df[score_columns].sum(axis=1)
    return pivot_df

def process(df):
    df[['Key Element Matching', 'Total Matched Key Elements', 'Score', 'Explanation']] = df['LLM_Response'].apply(  
        lambda x: pd.Series(process_llm_response(x))
    )
    df = organize_result(df)
    return df

def display(df, student_id):
    student_data = df[df["Student ID"] == student_id]
    
    if student_data.empty:
        st.warning("No data found for the selected student.")
        return

    question_numbers = sorted(
        {col.split("_")[0] for col in df.columns if col.startswith("Q") and "_Question" in col}
    )

    for question_number in question_numbers:
        question_text = student_data[f"{question_number}_Question"].iloc[0]
        marks_allocation = student_data[f"{question_number}_Marks Allocation"].iloc[0]
        rubric = student_data[f"{question_number}_Rubric"].iloc[0]
        student_answer = student_data[f"{question_number}_Student Answer"].iloc[0]
        key_element_matching = student_data[f"{question_number}_Key Element Matching"].iloc[0]
        explanation = student_data[f"{question_number}_Explanation"].iloc[0]
        score = student_data[f"{question_number}_Score"].iloc[0]

        with st.expander(f"{question_number}: {question_text}"):
            st.markdown(f"#### Marks Allocation: **{marks_allocation}**")
            
            st.markdown("#### Rubric:")
            try:
                rubric_dict = eval(rubric)  
                for points, description in rubric_dict.items():
                    st.markdown(f"- **{points}:** {description}")
            except Exception:
                st.markdown(f"```\n{rubric}\n```")
            
            st.markdown("#### Student Answer:")
            st.markdown(f"""{student_answer}""")
            
            st.markdown("#### Key Element Matching:")
            if isinstance(key_element_matching, str):
                key_element_matching_lines = key_element_matching.split("\n")
                for line in key_element_matching_lines:
                    st.markdown(f"{line.strip()}")
            else:
                st.markdown("No key element matching details available.")
            
            st.markdown("#### Explanation:")
            st.markdown(f"""{explanation}""")
            st.markdown(f"#### Score: **{score}**")

    total_marks = student_data["Total_Marks_Allocation"].iloc[0]
    total_score = student_data["Total_Score"].iloc[0]
    st.markdown(f"#### Total Score: {total_score}/{total_marks}")


