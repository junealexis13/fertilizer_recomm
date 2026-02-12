import streamlit as st
from fertilizer_recom import Fertilizers

def sidebar():
    with st.sidebar:
        st.header("Input Parameters")
        
        f_class = st.selectbox("Select Fertilizer Data Type", ["Predefined", "Custom"])

        if f_class == "Predefined":
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                N = st.selectbox("Select Fertilizer for N", ["UREA_PRILLED", "UREA_GRANULAR", "AMMOSUL", "COMPLETE"], key="N_default")
                st.session_state.fert_N = Fertilizers[N].value
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                P = st.selectbox("Select Fertilizer for P", ["DIAMMONIUM_PHOSPHATE", "AMMOPHOS"], key="P_default")
                st.session_state.fert_P = Fertilizers[P].value
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                K = st.selectbox("Select Fertilizer for K", ["MURIATE_OF_POTASH"], key="K_default")
                st.session_state.fert_K = Fertilizers[K].value

            st.caption('Choices limited to available fertilizers at DA-FPA market watch')
        else:
            st.text("Fertilizer for N")
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                N = st.number_input("Enter N", min_value=0, max_value=100, value=50, key="N_N")
                P = st.number_input("Enter P", min_value=0, max_value=100, value=50, key="N_P")
                K = st.number_input("Enter K", min_value=0, max_value=100, value=50, key="N_K")
                st.session_state.fert_N = {'N': N, 'P': P, 'K': K}
            st.text("Fertilizer for P")
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                N = st.number_input("Enter N", min_value=0, max_value=100, value=50, key="P_N")
                P = st.number_input("Enter P", min_value=0, max_value=100, value=50, key="P_P")
                K = st.number_input("Enter K", min_value=0, max_value=100, value=50, key="P_K")
                st.session_state.fert_P = {'N': N, 'P': P, 'K': K}
            st.text("Fertilizer for K")
            with st.container(border=True, horizontal=True, horizontal_alignment='left'):
                N = st.number_input("Enter N", min_value=0, max_value=100, value=50, key="K_N")
                P = st.number_input("Enter P", min_value=0, max_value=100, value=50, key="K_P")
                K = st.number_input("Enter K", min_value=0, max_value=100, value=50, key="K_K")
                st.session_state.fert_K = {'N': N, 'P': P, 'K': K}        