from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def call_openai_api(messages):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0 
    )
    return response.choices[0].message.content

def extract_rubric(extracted_text):
    prompt = f"""
    The following text is extracted from a document which contains a question, its answer key elements, and rubrics for grading. Extract and return them in JSON format with the following keys:
    - "question": The question being asked.
    - "key_elements": The key elements of the correct answer.
    - "rubric": The grading rubric for the question.

    Text:
    {extracted_text}
    """
    messages = [
        {"role": "system", "content": "You are an assistant that helps to extract question, answer key elements, and grading rubrics based on the provided text extracted from a document."},
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
            Your task involves analyzing the students' answer step by step to find matching key elements are matched and provide an accurate score based on the rubrics.
            Question: {question}
            Key Elements: {key_elements}
            Rubrics: {rubric}
            Student ID: {student_id}
            Student Answer: {student_answer}

            Step-by-step process:
            1. Analyze the student's answer phrase by phrase to identify potential matches for each key element.
            2. For each key element:
                - Determine if the key element is **fully matched**. A full match means that all important keywords or their synonyms in the key element are present in the student's answer.
                - Extract the exact part of the student's answer that matches the key element.
                - If the key element is not present, clearly state "No match."
            3. Summarize the total number of matched key elements.
            4. Based on the matched key elements, assign a score to the student's answer using the provided rubric.
            5. Provide a brief explanation for the assigned score, explaining how the score was derived.

             Provide the output in valid JSON format with the following structure, for key elements please state for all key elements:
            {{
                "Student ID": "{student_id}",
                "Student Answer": "{student_answer}",
                "Key Element Matching": [
                    {{
                        "Key Element": "<key element>",
                        "Matching Answer": "<matching part from student answer>"
                    }},
                    {{
                        "Key Element": "<key element>",
                        "Matching Answer": "No match"
                    }}
                ],
                "Total Matched Key Elements": <number of matched key elements>
                "Score": <score>,
                "Explanation": "<brief explanation for the score>"
            }}
            """
        }
    ]
    
    response = call_openai_api(messages_cot)
    return response


