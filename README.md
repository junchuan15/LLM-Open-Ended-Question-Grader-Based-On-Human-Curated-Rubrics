# **LLM-Based Automatic Grading of Open-Ended Questions Using Human-Curated Rubrics**  

This repository contains my Bachelor's Final Year Project (WIH3001 Data Science Project) at Universiti Malaya.



## **Project Overview**  

This project focuses on developing an **automated grading system** using **Large Language Models (LLMs)** to evaluate open-ended questions based on human-curated rubrics. The system is implemented using **Streamlit**, a Python-based web framework, and is powered by **OpenAI's GPT-4o Mini** model. 

By leveraging **prompt engineering**, various prompting techniques are applied to the LLM model to identify the most robust and reliable approach for the automated grading task. [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot) is identified as the best technique and is employed in the system, as it outperformed other prompting techniques across different performance metrics. The system is designed to be flexible, allowing users to upload their open-ended questions and rubrics from different domains to automate the grading process.



## **Key Features**  

1. **📂 Upload Rubrics**  
   - Extract questions, answer key elements, and rubrics from uploaded PDF documents.  

2. **📄 Analyze Multiple Student Answers**  
   - Supports batch uploads of student responses for parallel processing.  
    
3. **💾 Downloadable Reports**  
   - Generate ready-to-use grading reports in CSV format for future records or analysis.

4. **📊 Interactive Data Visualizations**  
   - Provides insights into grading performance through an interactive visualization dashboard.



## **Getting Started**  

### **1. Setting Up the Environment**  

Follow the steps below to set up the project:

#### **Step 1: Clone the repository and navigate to the project directory:**  

```bash
git clone https://github.com/junchuan15/LLM-Open-Ended-Question-Grader-Based-On-Human-Curated-Rubrics.git
cd LLM-Open-Ended-Question-Grader-Based-On-Human-Curated-Rubrics
```

#### **Step 2: Install the dependencies from the `requirements.txt` file using the following command:**  

```bash
pip install -r requirements.txt
```

---

### **2. Configuring the OpenAI API Key**  

To use the OpenAI API for grading responses, you must obtain an API key and configure it in the project. Follow these steps:

#### **Step 1: Get an OpenAI API Key**  

i. Go to [OpenAI's API page](https://platform.openai.com/signup) and sign up or log in.  
ii. Navigate to the **API keys** section under your account settings.  
iii. Generate a new API key and copy it.  

#### **Step 2: Add the API Key to the Project**  

Once you have the API key, store it in the `.env` file in the `src/` directory.  

i. Open the `.env` file in any text editor.  
ii. Replace `YOUR_OPENAI_API_KEY_HERE` with your actual API key. Example:

```makefile
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### **3. Running the Streamlit Application**  

After setting up the environment and API key, start the application by running the following command:

```bash
streamlit run main.py
```

---


## **Contact Information**  

For any inquiries or support, please contact:  
📧 **Email:** [22004851@siswa.um.edu.my](mailto:22004851@siswa.um.edu.my)




