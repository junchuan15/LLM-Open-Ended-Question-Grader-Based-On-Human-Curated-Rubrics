import json
import streamlit as st
import pandas as pd

def extract_match_and_score(response_text):
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
                                values=["Question", "Marks Allocation", "Student Answer", "Key Element Matching", "Score", "Explanation"])  

    pivot_df.columns = [f"{col[1]}_{col[0]}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    column_order = ["Student ID"]
    for index in sorted(set(df["Question_Label"])):
        column_order.extend([
            f"{index}_Question",
            f"{index}_Marks Allocation",
            f"{index}_Student Answer",
            f"{index}_Key Element Matching",
            f"{index}_Explanation",  # Corrected spelling
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
        lambda x: pd.Series(extract_match_and_score(x))
    )
    df = organize_result(df)
    return df

def display(df, student_id):
    for _, row in df.iterrows():
        for col_name, value in row.items():
            col1, col2, col3 = st.columns([1.1, 0.2, 6])  
            with col1:
                st.markdown(f"<span class='column-name'>{col_name}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span class='column-separator'>|</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"{value}")                         


