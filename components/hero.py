import streamlit as st


def hero():
    st.title("Fertilizer Recommendation System")
    st.write(":green[By: JA Santos] | :blue[For: Project SARAI and Project Sinag]")
    st.markdown("""
    <p style='text-align: justify; color: white;'>This application assists in calculating the optimal fertilizer combination for crops based on specific soil nutrient requirements. 
    Select from predefined fertilizer grades or input custom compositions to generate precise recommendations.</p>
    """, unsafe_allow_html=True)