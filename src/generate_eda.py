import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def histogram(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Total_Score'], bins=10, kde=True, color='Skyblue', alpha=0.7)
    plt.title('Student Score Distribution', fontsize=16)
    plt.xlabel('Total Score', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

def boxplot(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['Total_Score'], color='skyblue')
    plt.title("Box Plot of Total Scores")
    plt.xlabel("Total_Score")
    st.pyplot(plt)
