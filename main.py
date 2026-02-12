import streamlit as st
from components.sidebar import sidebar
from components.hero import hero
from components.state_handler import state_handler
from components.app import app

state_handler()
hero()
st.divider()
sidebar()

app()
