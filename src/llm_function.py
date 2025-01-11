from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def call_openai_api(messages, temperature=0.1):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"Error during OpenAI API call: {e}")

def extract_rubric(extracted_text):
    prompt = f"""
    The following text is extracted from a document, which contains multiple questions, their answer key elements, and rubrics for grading. 
    Extract and return them in JSON format as an array where each object has the following keys:
    - "question": The question being asked.
    - "marks_allocation": Marks allocated to the question. (integer)
    - "key_elements": The key elements of the correct answer as a list.
    - "rubric": The grading rubric for the question as a dictionary.

    Ensure each question is treated as a separate object in the array.
    Do not simplify the key elements, include all words as in the extracted text.
    Text:
    {extracted_text}
    """
    messages = [
        {"role": "system", "content": "You are an assistant that extracts multiple questions, their answer key elements, and grading rubrics from a provided document text."},
        {"role": "user", "content": prompt},
    ]

    response = call_openai_api(messages)
    return response

def grade_student_answer(question, key_elements, rubric, student_id, student_answer):
    messages_cot = [
        {
            "role": "system",
            "content": "You are an automated grader tasked to evaluate student answers step by step by matching them against predefined answer key elements and assigning a score based on the provided rubric."
        },
        {
            "role": "user",
            "content": f"""
            Question: {question}
            Key Elements: {key_elements}
            Rubrics: {rubric}
            Student ID: {student_id}
            Student Answer: {student_answer}

            Step-by-step process:
            1. Analyze the student's answer phrase by phrase to identify potential matches for each key element.
            2. For each key element:
                - Determine if the key element is **fully matched**. A full match means that all important keywords or their synonyms in the key element are present in the student's answer. Partially match or incomplete answer is not counted as a matched.
                - Extract the exact part of the student's answer that fully matches the key element.
                - If the key element is not present, clearly state "No match."
            3. Summarize the total number of matched key elements.
            4. Based on the matched key elements, assign a score to the student's answer using the provided rubric.
            5. Provide a short brief explanation for the assigned score, explaining how the score was derived.

             Provide the output in valid JSON format with the following structure, for key elements please state for all key elements:
{{
                "Student ID": "{student_id}",
                "Student Answer": "{student_answer}",
                "Key Element Matching": [
                    {{"Key Element": "<key element>" | "Matching Answer": "<matching part from student answer> or No match"}},
                ],
                "Score": <score>,
                "Explanation": "<brief explanation for the score>"
            }}
            """
        }
    ]
    
    response = call_openai_api(messages_cot)
    return response


