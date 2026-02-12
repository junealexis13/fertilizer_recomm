import streamlit as st

def state_handler():
    if "fert_N" not in st.session_state:
        st.session_state.fert_N = dict()
    if "fert_P" not in st.session_state:
        st.session_state.fert_P = dict()
    if "fert_K" not in st.session_state:
        st.session_state.fert_K = dict()

    if "recom_amount" not in st.session_state:
        st.session_state.recom_amount = dict()
