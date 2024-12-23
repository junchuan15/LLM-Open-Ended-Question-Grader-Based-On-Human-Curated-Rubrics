import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re

def calculate_metrics(df):
    metrics = [
        ("Average Score", f"{df['Total_Score'].mean():.2f}"),
        ("Max Score", df["Total_Score"].max()),
        ("Min Score", df["Total_Score"].min()),
        ("Median Score", f"{df['Total_Score'].median():.2f}"),
        ("Standard Deviation", f"{df['Total_Score'].std():.2f}"),
        ("Pass Percentage", f"{(df[df['Total_Score'] >= df['Total_Marks_Allocation'] / 2].shape[0] / df.shape[0]) * 100:.2f}%")
    ]
    return metrics


def scoretable(df):
    columns = [col for col in df.columns if col == "Student ID" or re.search(r"_Score$", col)]
    df = df[columns]
    st.markdown("#### Score Table")
    st.dataframe(df, use_container_width=True)
    
def histogram(df):
    st.markdown("#### Student Score Distribution")
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_alpha(0)  
    ax.patch.set_alpha(0)  
    sns.histplot(df['Total_Score'], bins=10, kde=True, color='#a7a7f3', alpha=0.7, ax=ax)
    ax.set_xlabel('Total Score', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

def boxplot(df):
    st.markdown("#### Boxplot of Scores")
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    fig.patch.set_alpha(0)  
    ax.patch.set_alpha(0)
    sns.boxplot(x=df['Total_Score'], color='#a7a7f3', ax=ax)
    ax.set_xlabel("Total Score", fontsize=10.5)
    st.pyplot(fig)

def areachart(df):
    st.markdown("#### Marks Allocation vs. Total Score")
    st.area_chart(
            data=df[["Total_Marks_Allocation", "Total_Score"]],
            color=['#a7a7f3','#8585ec'],
            use_container_width=True,
        )