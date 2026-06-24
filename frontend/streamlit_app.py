"""
frontend/streamlit_app.py - Main Streamlit Application
"""

import streamlit as st
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from frontend.components.sidebar import render_sidebar
from frontend.pages.home import render_home
from frontend.pages.case_details import render_case_details
from state.session_state import SessionState

st.set_page_config(
    page_title="AdalatMitra - AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SessionState.initialize()

def main():
    render_sidebar()
    
    page = st.session_state.get("page", "home")
    
    if page == "home":
        render_home()
    elif page == "case_details":
        render_case_details()
    else:
        render_home()
    
    st.divider()
    st.caption("⚖️ AdalatMitra v1.0.0 | Data from Delhi High Court")

if __name__ == "__main__":
    main()