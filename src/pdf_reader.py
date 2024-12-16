import PyPDF2
import pdfplumber

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
