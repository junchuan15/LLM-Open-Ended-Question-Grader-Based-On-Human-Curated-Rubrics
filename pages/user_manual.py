import streamlit as st
import os 
from src import loader

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/user_manual_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
st.markdown(
    f"""
    <div class="title-container">
        <img src="data:image/png;base64,{loader.load_image(img_path='assets/logo.trans.png')}" alt="Grady Logo">
        <div class="title">Grady - User Manual</div>
    </div>
    """, 
    unsafe_allow_html=True
)

def section (num, header, desc, img):
    st.markdown(f"""
    <div class="section">
        <div class="number">{num}</div>
        <div class="content">
            <div class="header">
            {header}
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
         "Please navigate to the 'Grading Hub' in the sidebar to start. To create a new assessment, enter the course code in the input field and press 'Enter' to proceed.", 
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

section(5, "Start Grading", 
        """Once the files are uploaded, click the "Grade" button to initiate the grading process. 
           Please note that the grading process may take a few minutes to complete, depending on the size and number of uploaded files.""", 
        loader.load_image(img_path='assets/step5.png'))

section(6, "View Grading Result", 
        """Once the grading process is completed, the results will be displayed in a tabular format for each file, allowing users to evaluate and review the grading outcomes. 
           Users can utilize the drop-down menu to select the specific answer they wish to view. The results include the question, marks allocation, answer matching, 
           graded score and an explanation for the assigned score.""", 
        loader.load_image(img_path='assets/step6.png'))

section(7, "Download Result", 
        """After reviewing the grading results, users can download the results in CSV format for their records. 
        Click the "Download" button to save the results, which include all the evaluated details for each uploaded answer.""", 
        loader.load_image(img_path='assets/step8.png'))

section(8, "Visualize Result", 
        """Users can navigate to the 'Visualization' tab to view the graphs and charts generated based on the overall total score results for the uploaded answers. 
           These visualizations provide valuable insights, allowing users to analyze overall performance trends, identify patterns and evaluate the grading outcomes effectively.""", 
        loader.load_image(img_path='assets/step8.png'))