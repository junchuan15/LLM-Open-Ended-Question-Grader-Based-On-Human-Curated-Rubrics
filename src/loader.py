import base64
import PyPDF2
import pdfplumber
import re

def load_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        pdf = f.read()
        base64_pdf = base64.b64encode(pdf).decode("utf-8")
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000px" style="border: none;"></iframe>
        """
        return pdf_display
        
def extract_pdf(file_obj):
    if isinstance(file_obj, str):
        pdfFileObj = open(file_obj, 'rb')
    else:
        pdfFileObj = file_obj

    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    combined_text = [] 

    try:
        with pdfplumber.open(pdfFileObj) as pdf:
            for pagenum in range(len(pdf.pages)):
                page_content = pdf.pages[pagenum]
                text = page_content.extract_text()
                if text:
                    combined_text.append(text)

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")

    finally:
        if isinstance(file_obj, str):
            pdfFileObj.close()

    return "\n".join(combined_text)

def extract_student_answers(extracted_text, rubric_result):
    questions = [item.get("question", "") for item in rubric_result if "question" in item]
    answers = re.split(r'\n*\d+\.\s*', extracted_text.strip())[1:] 
    result = []
    for i, question in enumerate(questions):
        answer = answers[i].strip() if i < len(answers) and answers[i].strip() else "No answer provided."
        result.append({"question": question, "student_answer": answer})

    return result
