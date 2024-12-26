import streamlit as st
import os 
from src import loader
import base64

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/user_manual_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def section (num, title, desc, img):
    st.markdown(f"""
    <div class="section">
        <div class="number">{num}</div>
        <div class="content">
            <div class="title">
            {title}
            </div>
            <div class="description">
               {desc}
            </div>
        </div>
    </div>
    <div class="image">
        <img src="data:image/png;base64,{img}" alt="Feature 1">
    </div>
""", unsafe_allow_html=True)
    
section (1,"Create a New Assessment", 
         "To create a new assessment, enter the course code in the input field and press 'Enter' to proceed.", 
         loader.load_image(img_path = 'assets/step1.png'))

section (2,"Upload Rubric", 
         """Click the 'Browse files' button to upload the rubric file (.pdf) from your local machine. Ensure the rubric includes the following details: 
            questions, mark allocations, sample answers, and rubrics with descriptions for each mark distribution. It is important 
            that the rubric provides clear criteria for grading. Multiple questions can be included in a single file, but each question's rubric must 
            be well-organized and easy to identify. You may tick the checkbox below to view the sample of rubric file format.""", 
         loader.load_image(img_path = 'assets/step2.png'))

view_rubric = st.checkbox("View Sample Rubric File")
if view_rubric:
    st.markdown(loader.display_pdf("assets/sample_rubric.pdf"), unsafe_allow_html=True)
    
section(3, "View Rubric", 
        """After the system finishes loading the question, it will display the details of each question along with their respective rubrics.
        Click on the "Question" tab to view the details and ensure the system has extracted the correct information. In case the system fails to extract the relevant information,
        users are advised to reformat the rubric file according to the sample file provided above to ensure the system performs perfectly.""", 
        loader.load_image(img_path='assets/step3.png'))

section(4, "Upload Answer", 
        """Next, click the "Grade Answer" tab in the navigation bar to proceed with uploading the answers. 
           Click the "Browse files" button to upload the answer files (.pdf) from your local machine.
           Ensure that the uploaded answer files contain responses to all the questions listed in the uploaded rubric. 
           Multiple answer files are supported, allowing batch processing for the grading task. The file name will be treated as Student ID.""", 
        loader.load_image(img_path='assets/step4.png'))

view_answer = st.checkbox("View Sample Answer File")
if view_answer:
    st.markdown(loader.display_pdf("assets/sample_answer.pdf"), unsafe_allow_html=True)
