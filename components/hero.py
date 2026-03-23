import streamlit as st

def hero():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("images/sinag_logo.png", width=120)
    with col2:
        st.title("Fertilizer Recommendation")
        
    st.markdown("### <span style='color: #E59A00;'>Project SARAI</span> & <span style='color: #01426A;'>Project Sinag</span>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: justify; color: #555555; font-size: 1.1rem; line-height: 1.6; margin-top: 10px;'>
    This application assists in calculating the optimal fertilizer combination for crops based on specific soil nutrient requirements. 
    Select from predefined fertilizer grades or input custom compositions to generate precise recommendations.
    </p>
    """, unsafe_allow_html=True)