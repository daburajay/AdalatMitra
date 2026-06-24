"""
frontend/pages/home.py - Home Page
"""

import streamlit as st
from frontend.components.search_form import render_search_form
from frontend.components.case_display import render_case_display


def render_home():
    """Render home page."""

    st.title("⚖️ AdalatMitra")
    st.caption("Your AI Legal Assistant for Indian Courts")

    # Info box
    with st.expander("ℹ️ How to use", expanded=False):
        st.markdown("""
        **Search for court cases by:**
        1. **Party Name** - Enter any party name (petitioner or respondent)
        2. **Status** - Filter by case status (Pending, Listed, Disposed, etc.)
        3. **Year** - Filter by filing year

        **What you get:**
        - Complete case details
        - CNR number
        - Party information
        - Next hearing date
        """)

        st.divider()

        # Search form
        render_search_form()

        # Display results
        st.divider()
        render_case_display()
