"""
state/session_state.py - Session State Management
"""

import streamlit as st
from typing import Dict, Any, List, Optional

class SessionState:
    """Manage session state for the application."""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables."""
        if "initialized" not in st.session_state:
            st.session_state.initialized = True
            
            # User preferences
            st.session_state.language = "english"
            st.session_state.court = "Delhi High Court"
            
            # Search state
            st.session_state.search_results = []
            st.session_state.search_query = {}
            st.session_state.selected_case = None
            
            # Page state
            st.session_state.page = "home"
            
            # Chat state
            st.session_state.chat_history = []
            st.session_state.chat_enabled = False