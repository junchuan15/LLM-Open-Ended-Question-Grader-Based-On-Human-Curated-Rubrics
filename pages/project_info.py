import streamlit as st
import os
from src import loader
import pandas as pd

# --- Load CSS ---
css_path = os.path.join(os.path.dirname(__file__), "../styles/project_info_page.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="title-container">
        <img src="data:image/png;base64,{loader.load_image(img_path='assets/logo.trans.png')}" alt="Grady Logo">
        <div class="title">Grady - Project Info</div>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("""
    <div class="h1">Overview</div>
    <div class="description">
        This project focuses on developing <strong>automated grading systems</strong> using <strong>large language models (LLMs)</strong> to evaluate 
        <strong>open-ended questions</strong> based on <strong>human-curated rubrics</strong>. By leveraging <strong>prompt engineering</strong>, various 
        prompting techniques are applied to the LLM model to identify the most robust and reliable approach for the automated grading task, 
        based on evaluation across different performance metrics. The system is also designed to be flexible, 
        allowing users to upload their own open-ended questions and rubrics from different domains to automate the grading process.
    </div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="h1">About Dataset</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,3])

with col1:
    st.markdown("""
    <div class="column-content" style="margin-top: 20px;">
        <h2>Data Source</h2>
        <div class="image-container" style="margin-bottom: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/Kaggle_logo.png" alt="Kaggle Logo">
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.text("ASAP-SAS (Automated Student Assessment Prize - Short Answer Scoring)")


with col2:
    st.markdown("""
    <div class="column-content">
        <h2>Description</h2>
        <p class="description">
            The original dataset obtained contains 10 open-ended questions in a <strong>docx</strong> file 
            related to Science, English, Art, and Biology, along with a list of students' answers with 
            human-graded scores for each question in a <strong>CSV</strong> file. This project only includes 
            <strong>Question 5</strong> & <strong>Question 6</strong> as they meet the requirement of having 
            sample answers with defined grading rubrics.
        </p>
        <h2>Dataset Size</h2>
    </div>
    """, unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric(label="Total Questions", value="10")
    with metric_col2:
        st.metric(label="Selected Questions", value="2 (Q5,Q6)")
    with metric_col3:
        st.metric(label="Total Answer Responses (After Sampling)", value="304")
    with metric_col4:
        st.metric(label="Score label", value="4")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="h1">Model Info</div>
<div class="description">
    The selected LLM for this project is <strong>GPT-4.0 Mini</strong>, a compact and efficient variant of OpenAI's GPT-4.0 series. 
    It offers high-quality language understanding and generation capabilities while optimizing resource efficiency, 
    making it ideal for lightweight applications such as automated grading tasks. Its ability to handle nuanced contexts 
    and align responses with predefined rubrics ensures accurate and consistent evaluation.
</div>

<div class="h1" style="margin-top: 30px;">Prompt Engineering</div>
<div class="description" style="margin-bottom: 10px;">
    Prompt engineering is the art and science of designing and optimizing prompts to guide AI models, 
    particularly LLMs, towards generating the desired responses. This project utilised <strong>3 different prompting techniques: Zero-shot, Chain-of-Thought, and Reflexion</strong> 
    in order to select the best technique to be applied on grading open-ended questions based on human-curated rubrics. 
    The best prompting technique will be chosen based on testing it on the chosen dataset and evaluating its performance using predefined metrics.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='prompting-container'>
    <div class='grid'>
        <div class="grid-item">
            <div class="grid-header">01. Zero Shot Prompting</div>
            <div class="grid-content">A technique in which the LLM model is provided with a task description or query without prior examples to generate an appropriate response.</div>
        </div>
        <div class="grid-item">
            <div class="grid-header">02. Chain-of-Thought (CoT)</div>
            <div class="grid-content">A technique in which the model is guided to solve complex problems by breaking them down into smaller, logical components.</div>
        </div>
        <div class="grid-item">
            <div class="grid-header">03. Reflexion (Self-Reflection)</div>
            <div class="grid-content">A technique in which the model re-evaluates its own outputs, identifies potential errors or areas for improvement, and iteratively revises its responses to achieve more accurate results.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown("""
    <div class="h1">Evaluation Results</div>
    <div class="description" style="margin-bottom: 20px;">
        The performance of different prompting techniques applied to the <strong>GPT-4o Mini</strong> LLM model is evaluated using <strong>5 key performance metrics: Accuracy, Precision, Recall, F1 Score, and Quadratic Weighted Kappa (QWK).</strong> 
        The best prompting technique is selected based on these metrics to ensure optimal grading accuracy and consistency. The result of evaluation are as shown below:
    </div>
""", unsafe_allow_html=True)

data = {
    "Prompting Technique": ["Zero-shot", "Chain-of-Thought", "Reflexion"],
    "Accuracy": [0.625, 0.763, 0.641],
    "F1 Score": [0.627, 0.764, 0.646],
    "Precision": [0.635, 0.766, 0.656],
    "Recall": [0.625, 0.763, 0.641],
    "Quadratic Weighted Kappa": [0.752, 0.871, 0.782],
}

df = pd.DataFrame(data)

st.table(df)
st.markdown("""
    <div class="description">
        Based on the evaluation results, the <strong>Chain-of-Thought (CoT)</strong> prompting technique is selected as the most effective for 
        the automated grading task. It achieved the highest scores across key performance metrics, including 
        <strong>Accuracy (0.763)</strong>, <strong>F1 Score (0.764)</strong>, <strong>Precision (0.766)</strong>, and <strong>Quadratic Weighted Kappa (0.871)</strong>. 
        Its ability to decompose complex tasks into logical steps ensures that the grading process is both accurate and consistent with human-curated rubrics, 
        making it the optimal choice for evaluating open-ended questions.
    </div>
""", unsafe_allow_html=True)
