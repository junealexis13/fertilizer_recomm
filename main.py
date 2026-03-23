import streamlit as st

st.set_page_config(
    page_title="Fertilizer Recommendation | DOST Sinag",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        p, div[data-testid="stMarkdownContainer"] {
            color: #333333;
        }
        div[data-testid="metric-container"] label,
        div[data-testid="stMetricValue"] {
            color: #01426A;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #01426A !important;
            font-weight: 700 !important;
        }
        .stButton>button {
            background-color: #FCAF17;
            color: #01426A !important;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            background-color: #E59A00;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #EBEBEB !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            background-color: #FFFFFF;
        }
        code {
            color: #E59A00 !important;
        }
        [data-testid="stSidebar"] hr {
            border-bottom: 1px solid #005F99;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #FCAF17 !important;
        }
        /* Fix text in sidebar elements */
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] input {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #FFFFFF !important;
        }

        button[data-testid="stNumberInputStepDown"] {
            color: #ff9e9e !important;
        }

        button[data-testid="stNumberInputStepUp"] {
            color: #94fa91 !important;
        }

        .stApp input {
            color: #ffffff;
        }
        
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

local_css()

from components.sidebar import sidebar
from components.hero import hero
from components.state_handler import state_handler
from components.app import app

state_handler()
st.write("") # some space
hero()
st.divider()
sidebar()

app()
