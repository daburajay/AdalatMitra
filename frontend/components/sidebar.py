"""
frontend/components/sidebar.py - Sidebar Component
"""

import streamlit as st
from utils.constants import LANGUAGE_OPTIONS

def render_sidebar():
    """Render sidebar with navigation and settings."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/justice.png", width=80)
        st.title("⚖️ AdalatMitra")
        st.caption("v1.0.0")
        
        st.divider()
        
        # Navigation
        pages = {
            "🏠 Home": "home",
            "🔍 Search": "search",
            "📄 Upload PDF": "pdf",
            "⚙️ Settings": "settings"
        }
        
        for label, page_id in pages.items():
            if st.button(label, width="stretch", key=f"nav_{page_id}"):
                st.session_state.page = page_id
                st.rerun()
        
        st.divider()
        
        # Language selector
        st.subheader("🌐 Language")
        current_lang = st.session_state.get("language", "english")
        
        lang_options = list(LANGUAGE_OPTIONS.keys())
        try:
            current_index = lang_options.index(current_lang)
        except ValueError:
            current_index = 0
        
        selected = st.selectbox(
            "Select Language",
            options=lang_options,
            format_func=lambda x: LANGUAGE_OPTIONS.get(x, x),
            index=current_index,
            key="language_selector"
        )
        
        if selected != current_lang:
            st.session_state.language = selected
            st.rerun()
        
        st.divider()
        
        # Status
        st.caption("🔐 API Status")
        st.caption("✅ Delhi High Court Connected")
        st.caption("✅ AI Gateway Active")
        
        st.divider()
        st.caption("📞 Help: contact@adalatmitra.com")