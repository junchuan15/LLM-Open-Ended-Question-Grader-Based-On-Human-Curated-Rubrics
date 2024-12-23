import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def histogram(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_alpha(0)  
    ax.patch.set_alpha(0)  
    sns.histplot(df['Total_Score'], bins=10, kde=True, color='#a7a7f3', alpha=0.7, ax=ax)
    #ax.set_title('Student Score Distribution', fontsize=12)
    ax.set_xlabel('Total Score', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

def boxplot(df):
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    fig.patch.set_alpha(0)  
    ax.patch.set_alpha(0)
    sns.boxplot(x=df['Total_Score'], color='#a7a7f3', ax=ax)
    #ax.set_title("Box Plot of Total Scores", fontsize=12)
    ax.set_xlabel("Total Score", fontsize=10.5)
    st.pyplot(fig)
