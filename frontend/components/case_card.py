"""
frontend/components/case_card.py - Clean Case Card
"""

import streamlit as st

def render_case_card(case_data: dict, index: int = None):
    """Render a clean case card."""
    
    # Extract data
    case_number = case_data.get("case_number", "N/A")
    case_type = case_data.get("case_type", "N/A")
    cnr_number = case_data.get("cnr_number", "N/A")
    petitioner = case_data.get("petitioner", "N/A")
    respondent = case_data.get("respondent", "N/A")
    status = case_data.get("status", "Unknown")
    next_hearing = case_data.get("next_hearing", "Not scheduled")
    court = case_data.get("court", "Delhi High Court")
    
    # Status color
    status_colors = {
        "pending": "#ff4b4b",
        "listed": "#ffa500",
        "disposed": "#00cc66",
        "dismissed": "#808080",
        "institution": "#2196F3",
    }
    status_lower = status.lower()
    color = status_colors.get(status_lower, "#4a6fa5")
    
    with st.container():
        # Card header
        col1, col2, col3 = st.columns([2, 1, 1.5])
        with col1:
            st.markdown(f"**📋 {case_number}**")
        with col2:
            st.caption(f"*{case_type}*")
        with col3:
            st.markdown(f"""
            <span style="
                background: {color};
                color: white;
                padding: 2px 14px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            ">{status.upper()}</span>
            """, unsafe_allow_html=True)
        
        # Parties
        col1, col2 = st.columns(2)
        with col1:
            st.caption("👤 **Petitioner**")
            st.text(petitioner[:60] + ('...' if len(petitioner) > 60 else ''))
        with col2:
            st.caption("👥 **Respondent**")
            st.text(respondent[:60] + ('...' if len(respondent) > 60 else ''))
        
        # Footer
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"📋 CNR: {cnr_number}")
        with col2:
            st.caption(f"🏛️ {court}")
        with col3:
            st.caption(f"📅 Next: {next_hearing}")
        
        # Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 View Details", key=f"view_{case_number}", use_container_width=True):
                st.session_state.selected_case = case_data
                st.session_state.page = "case_details"
                st.rerun()
        with col2:
            if st.button("💬 Ask AI", key=f"askai_{case_number}", use_container_width=True):
                st.session_state.selected_case = case_data
                st.session_state.page = "case_details"
                # Scroll to chat section
                st.rerun()
        
        st.divider()