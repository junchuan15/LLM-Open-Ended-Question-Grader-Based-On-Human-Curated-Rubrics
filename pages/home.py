import streamlit as st
import os 
from src import loader

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/home_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

logo = loader.load_image(img_path = 'assets/logo.bg.png')

st.markdown(f'''
<div class="logo-container">
    <img src="data:image/png;base64,{logo}" class="logo" alt="Logo">
</div>
<div class="text-container">
    <span class="title-text">
        Replace Your <strong class="red-pen">Red Pen ✍️</strong> with Just a <strong class="green-clicks">Few Simple Clicks 🖱️</strong>
    </span>
    <span class="description-text">
        <br><strong>Meet Grady – Your Trusted AI-Powered Grading Assistant.</strong><br>
        Leveraging the power of Large Language Model (LLM), Grady transforms your grading experience on open-ended questions by reducing manual workload, ensuring fairness, and personalizing assessments to match your unique needs.
    </span>
</div>
''', unsafe_allow_html=True)


st.markdown("""
<div id="key-features" style="margin-top: 3rem; "margin-bottom: 2rem;">
    <div class='h1'>
     Key Features
     </div>
<div class="features-grid-container">
    <div class="feature-item">
        <div class="feature-content">
            <div class="feature-title">📂 Upload Rubrics</div>
            <div class="feature-desc">
                User are allowed to uplopad pre-defined grading rubrics with clear criteria and answer for evaluation.
            </div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-content">
            <div class="feature-title">📄 Analyze Student Answers</div>
            <div class="feature-desc">
                Upload student responses in batches, and let the system intelligently evaluate and score each answer.
            </div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-content">
            <div class="feature-title">📊 Interactive Data Visualizations</div>
            <div class="feature-desc">
                Gain deeper insights into class performance with visualization diagrams.
            </div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-content">
            <div class="feature-title">💾 Downloadable Reports</div>
            <div class="feature-desc">
                Generate comprehensive, ready-to-use grading reports in CSV format for future records or analysis.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='h1'>
     Project Objectives
     </div>
    <div class='objectives-container'>
        <div class="card">
            <div class='card-text'>
                <span class='card-title'>01.</span>
                <span class='card-desc'>To <b>develop</b> an LLM-based grading model that evaluate open-ended questions based on human-curated rubrics.</span>
            </div>
        </div>
        <div class="card">
            <div class='card-text'>
                <span class='card-title'>02.</span>
                <span class='card-desc'>To <b>evaluate</b> the performance of the LLM-based grading model  across different prompting techniques.</span>
            </div>
        </div>
        <div class="card">
            <div class='card-text'>
                <span class='card-title'>03.</span>
                <span class='card-desc'>To <b>deploy</b> a web application which can automate the grading of open-ended questions based on uploaded rubrics.</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="h1">Why Choose Grady ?</div>
<div class="advantages-container">
    <div class="card">
        <div class="card-text">
            <span class="card-title">⏱️ Save Time</span>
            <span class="card-desc">
                Automate grading of open-ended questions, saving hours of manual effort.
            </span>
        </div>
    </div>
    <div class="card">
        <div class="card-text">
            <span class="card-title">⚖️ Ensure Fairness</span>
            <span class="card-desc">
                Consistent scoring based on predefined rubrics ensures objective and fair evaluations.
            </span>
        </div>
    </div>
    <div class="card">
        <div class="card-text">
            <span class="card-title">📊 Actionable Insights</span>
            <span class="card-desc">
                Interactive dashboards provide detailed performance analysis for better decision-making.
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



