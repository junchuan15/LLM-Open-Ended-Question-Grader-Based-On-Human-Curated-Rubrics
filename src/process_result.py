import json
import pandas as pd

def extract_match_and_score(response_text):
    matched_key_elements = 0
    score = None
    key_element_matches_formatted = ""

    try:
        response_data = json.loads(response_text)
        key_element_matches = response_data.get("Key Element Matching", [])
        matched_key_elements = response_data.get("Total Matched Key Elements", 0)
        score = response_data.get("Score", None)

        key_element_matches_formatted = "\n".join(
            [f"- Key Element: {match['Key Element']}\n  Matching Answer: {match['Matching Answer']}" 
             for match in key_element_matches]
        )

    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response_text}")
        key_element_matches_formatted = "Error decoding JSON"

    return key_element_matches_formatted, matched_key_elements, score

def extract(df):
    # Apply the function and store in new columns
    df[['Key Element Matching', 'Total Matched Key Elements', 'Score']] = df['LLM_Response'].apply(
        lambda x: pd.Series(extract_match_and_score(x))
    )
    return df

