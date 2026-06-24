"""
frontend/components/case_display.py - Complete Case Display with Fixed Status
"""

import streamlit as st
from frontend.components.case_card import render_case_card

def render_case_display():
    """Render case results with working filter."""
    
    cases = st.session_state.get("search_results", [])
    query = st.session_state.get("search_query", {})
    
    if not cases:
        st.info("🔍 Search for cases using the form above")
        return
    
    # Show court type badge
    court_type = query.get("court_type", "High Court")
    if court_type == "District Court":
        st.info(f"🏛️ **District Court**: {query.get('state', '')} - {query.get('district', '')}")
    
    # Summary
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Cases", len(cases))
    with col2:
        st.metric("👤 Party", query.get("party_name", "N/A"))
    with col3:
        st.metric("📅 Year", query.get("year", "N/A"))
    with col4:
        st.metric("📌 Status", query.get("status", "N/A"))
    
    st.markdown("---")
    
    # Status breakdown - Use search status instead of API status
    # Since API doesn't return status, we use the filter status
    search_status = query.get("status", "Pending")
    
    st.subheader("📊 Status Breakdown")
    cols = st.columns(1)
    with cols[0]:
        st.markdown(f"**{search_status}**")
        st.caption(f"{len(cases)} cases")
    
    st.markdown("---")
    
    # Advanced Filters - returns filtered cases
    filtered_cases = render_filters(cases, search_status)
    
    # Display cases
    if filtered_cases:
        for i, case in enumerate(filtered_cases, 1):
            render_case_card(case, i)
    else:
        st.warning("No cases match the selected filters")
    
    # Export
    if filtered_cases:
        st.markdown("---")
        st.subheader("📤 Export Data")
        
        if st.button("📥 Download JSON", use_container_width=True):
            import json
            json_str = json.dumps(filtered_cases, indent=2, default=str)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"cases_{query.get('party_name', 'search')}.json",
                mime="application/json",
                use_container_width=True
            )


def render_filters(cases, default_status="Pending"):
    """Render advanced filters and return filtered cases."""
    
    # Get unique statuses from cases (if any), otherwise use default
    status_options = list(set([c.get("status", "").strip() for c in cases if c.get("status", "").strip()]))
    
    # If no status in cases, use the search status
    if not status_options:
        status_options = [default_status, "Disposed"]
    
    # Ensure default_status is in options
    if default_status not in status_options:
        status_options.insert(0, default_status)
    
    filter_key = f"filter_{hash(str(cases))}"
    
    st.markdown("""
    <style>
    .filter-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 16px 0 24px 0;
        border: 1px solid #eef2f7;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .filter-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f3a5f;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .filter-label {
        font-size: 13px;
        font-weight: 500;
        color: #555;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🔍 Advanced Filters</div>', unsafe_allow_html=True)
        
        # Row 1: 2 Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="filter-label">📋 Case Number</div>', unsafe_allow_html=True)
            case_number_filter = st.text_input(
                "Case Number",
                placeholder="e.g., 282/2019",
                key=f"case_number_filter_{filter_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<div class="filter-label">🔑 CNR Number</div>', unsafe_allow_html=True)
            cnr_filter = st.text_input(
                "CNR Number",
                placeholder="e.g., DLHC010166842019",
                key=f"cnr_filter_{filter_key}",
                label_visibility="collapsed"
            )
        
        # Row 2: 2 Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="filter-label">👤 Party Name</div>', unsafe_allow_html=True)
            party_filter = st.text_input(
                "Party Name",
                placeholder="e.g., LAXMAN SHARMA",
                key=f"party_filter_{filter_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<div class="filter-label">📌 Status</div>', unsafe_allow_html=True)
            # Use default selection as the search status
            default_selection = [default_status] if default_status in status_options else status_options[:1]
            selected_statuses = st.multiselect(
                "Status",
                options=status_options,
                default=default_selection,
                key=f"status_filter_{filter_key}",
                label_visibility="collapsed"
            )
        
        # Row 3: Sort Only
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="filter-label">📊 Sort By</div>', unsafe_allow_html=True)
            sort_by = st.selectbox(
                "Sort By",
                ["Case Number", "Case Type", "Petitioner", "Respondent", "CNR Number"],
                key=f"sort_by_{filter_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<div class="filter-label"> </div>', unsafe_allow_html=True)
            active_filters = 0
            if case_number_filter:
                active_filters += 1
            if cnr_filter:
                active_filters += 1
            if party_filter:
                active_filters += 1
            if selected_statuses and len(selected_statuses) < len(status_options):
                active_filters += 1
            
            if active_filters > 0:
                st.caption(f"🔍 {active_filters} filter(s) active")
            else:
                st.caption("📋 Showing all cases")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_cases = cases.copy()
    
    if case_number_filter:
        filtered_cases = [c for c in filtered_cases if case_number_filter.lower() in c.get("case_number", "").lower()]
    
    if cnr_filter:
        filtered_cases = [c for c in filtered_cases if cnr_filter.lower() in c.get("cnr_number", "").lower()]
    
    if party_filter:
        party_lower = party_filter.lower()
        filtered_cases = [
            c for c in filtered_cases 
            if party_lower in c.get("petitioner", "").lower() or party_lower in c.get("respondent", "").lower()
        ]
    
    if selected_statuses:
        # If cases have status, filter by it, otherwise keep all (since we don't have status)
        has_status = any(c.get("status", "").strip() for c in filtered_cases)
        if has_status:
            filtered_cases = [c for c in filtered_cases if c.get("status", "").strip() in selected_statuses]
        # If no status in cases, we keep all (status filter doesn't apply)
    
    if sort_by == "Case Number":
        filtered_cases.sort(key=lambda x: x.get("case_number", ""))
    elif sort_by == "Case Type":
        filtered_cases.sort(key=lambda x: x.get("case_type", ""))
    elif sort_by == "Petitioner":
        filtered_cases.sort(key=lambda x: x.get("petitioner", ""))
    elif sort_by == "Respondent":
        filtered_cases.sort(key=lambda x: x.get("respondent", ""))
    elif sort_by == "CNR Number":
        filtered_cases.sort(key=lambda x: x.get("cnr_number", ""))
    
    # Show count
    st.caption(f"Showing {len(filtered_cases)} of {len(cases)} cases")
    
    if not filtered_cases:
        st.warning("❌ No cases match the selected filters")
    
    return filtered_cases