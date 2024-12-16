import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def score_histogram(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df['Score'], bins=range(min(df['Score']), max(df['Score']) + 2), edgecolor='black', color='skyblue')
    plt.title("Histogram of Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

def score_boxplot(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['Score'], color='lightgreen')
    plt.title("Box Plot of Scores")
    plt.xlabel("Score")
    st.pyplot(plt)

def visualization_report(df):
    score_histogram(df)
    score_boxplot(df)