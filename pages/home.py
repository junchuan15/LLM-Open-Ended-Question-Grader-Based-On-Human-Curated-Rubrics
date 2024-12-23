import streamlit as st
import os 
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/home_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

logo = get_base64_image(img_path = 'assets/logo1200.png')


st.markdown(f'''
<div class="title-container">
    <div class="logo-container">
        <img src="data:image/png;base64,{logo}" class="logo" alt="Logo">
    </div>
    <span class="title-text">
        Replace Your <strong class="red-pen">Red Pen ✍️</strong> with Just a <strong class="green-clicks">Few Simple Clicks 🖱️</strong>
    </span>
        <p class="title-description">
        <strong>Meet Grady – Your Trusted AI-Powered Grading Assistant.</strong>
        Leveraging the power of Large Language Model (LLM), transforms your grading experience on open-ended questions by reducing manual workload, ensuring fairness, and personalizing assessments to match your unique needs.
    </p>
    <div class="get-started-frame">
        <div class="get-started-container">
            <a href="#key-features" class="get-started-arrow">↓</a>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)


st.markdown("""
<div id="key-features" style="margin-top: 3rem;">
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
                <span class='card-desc'>To <b>develop</b> an LLM-based automated grading system for evaluating open-ended questions using human-curated rubrics.</span>
            </div>
        </div>
        <div class="card">
            <div class='card-text'>
                <span class='card-title'>02.</span>
                <span class='card-desc'>To <b>evaluate</b> the performance of the LLM-based grading model across different prompting techniques.</span>
            </div>
        </div>
        <div class="card">
            <div class='card-text'>
                <span class='card-title'>03.</span>
                <span class='card-desc'>To <b>visualize</b> student performance on the grading results using Exploratory Data Analysis (EDA).</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)