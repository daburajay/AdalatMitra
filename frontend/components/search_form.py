"""
frontend/components/search_form.py - Search Form with Court Type Selection
"""

import streamlit as st
import asyncio
from services.bharat_court_service import BharatCourtService
from services.district_court_service import DistrictCourtService
from utils.constants import STATUS_FILTERS

def render_search_form():
    """Render the case search form with court type selection."""
    
    st.subheader("🔍 Search Cases")
    
    # Court Type Selection
    court_type = st.radio(
        "Select Court Type:",
        ["High Court", "District Court"],
        horizontal=True,
        key="court_type"
    )
    
    if court_type == "High Court":
        render_high_court_search()
    else:
        render_district_court_search()


def render_high_court_search():
    """Render High Court search form - KEEP UNCHANGED!"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        party_name = st.text_input(
            "Party Name",
            placeholder="e.g., Union of India, LAXMAN, SACHIN",
            key="hc_party_search_input"
        )
    
    with col2:
        year = st.text_input("Year", value="2024", key="hc_year_input")
    
    status = st.selectbox(
        "Status Filter",
        options=["Pending", "Listed", "Disposed", "Dismissed", "Institution", "All"],
        key="hc_status_filter"
    )
    
    # HIGH COURT SEARCH - DO NOT CHANGE THIS!
    if st.button("🔍 Search High Court", type="primary", use_container_width=True):
        if not party_name:
            st.error("Please enter a party name")
            return
        
        with st.spinner(f"🔍 Searching for '{party_name}'..."):
            try:
                service = BharatCourtService(court_name="Delhi High Court")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    service.search_cases(
                        party_name=party_name.strip(),
                        year=year.strip(),
                        status=status
                    )
                )
                loop.close()
                
                if result.get("success"):
                    cases = result.get("cases", [])
                    st.session_state.search_results = cases
                    st.session_state.search_query = {
                        "party_name": party_name,
                        "year": year,
                        "status": status,
                        "total": len(cases),
                        "court_type": "High Court"
                    }
                    st.success(f"✅ Found {len(cases)} cases")
                    st.rerun()
                else:
                    st.error(f"❌ {result.get('error', 'Search failed')}")
                    
            except Exception as e:
                st.error(f"❌ Search failed: {str(e)}")


def render_district_court_search():
    """Render District Court search form - NEW ADDITION."""
    
    state_options = {
        "7": "Delhi",
        "8": "Bihar", 
        "27": "Maharashtra",
        "34": "Tamil Nadu",
        "29": "Karnataka",
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_state = st.selectbox(
            "Select State",
            options=list(state_options.keys()),
            format_func=lambda x: state_options.get(x, x),
            key="dc_state_select"
        )
    
    with col2:
        district_options = {
            "7": {"1": "Central Delhi"},
            "8": {"1": "Patna"},
            "27": {"1": "Mumbai"},
            "34": {"1": "Chennai"},
            "29": {"1": "Bangalore"},
        }
        districts = district_options.get(selected_state, {"1": "Default"})
        selected_district = st.selectbox(
            "Select District",
            options=list(districts.keys()),
            format_func=lambda x: districts.get(x, x),
            key="dc_district_select"
        )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        party_name = st.text_input(
            "Party Name",
            placeholder="e.g., Sir Sobha Singh, Indian Electricals",
            key="dc_party_search_input"
        )
    
    with col2:
        year = st.text_input("Year", value="2024", key="dc_year_input")
    
    status = st.selectbox(
        "Status Filter",
        options=["Pending", "Disposed", "All"],
        key="dc_status_filter"
    )
    
    st.caption("💡 District Court search auto-discovers the court complex.")
    
    if st.button("🔍 Search District Court", type="primary", use_container_width=True):
        if not party_name:
            st.error("Please enter a party name")
            return
        
        with st.spinner(f"🔍 Searching for '{party_name}'..."):
            try:
                service = DistrictCourtService()
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    service.search_cases(
                        party_name=party_name.strip(),
                        state_code=selected_state,
                        district_code=selected_district,
                        year=year.strip(),
                        status=status
                    )
                )
                loop.close()
                
                if result.get("success"):
                    cases = result.get("cases", [])
                    if cases:
                        st.session_state.search_results = cases
                        st.session_state.search_query = {
                            "party_name": party_name,
                            "year": year,
                            "status": status,
                            "total": len(cases),
                            "court_type": "District Court",
                            "state": state_options.get(selected_state, selected_state),
                            "district": districts.get(selected_district, selected_district)
                        }
                        st.success(f"✅ Found {len(cases)} cases")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ No cases found for '{party_name}' in year {year}")
                else:
                    st.error(f"❌ {result.get('error', 'Search failed')}")
                    
            except Exception as e:
                st.error(f"❌ Search failed: {str(e)}")