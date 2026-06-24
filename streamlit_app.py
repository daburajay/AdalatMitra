import streamlit as st

from agents.case_agent import track_case
from agents.explanation_agent import explain_legal_text
from config.languages import SUPPORTED_LANGUAGES
from agents.timeline_agent import get_case_timeline, explain_timeline

st.set_page_config(page_title="AdalatMitra", layout="wide")
st.title("⚖ AdalatMitra")

language = st.selectbox("Choose Language", list(SUPPORTED_LANGUAGES.keys()))
st.divider()

# --- Initialize session state ---
if "case_data" not in st.session_state:
    st.session_state.case_data = None
if "timeline" not in st.session_state:
    st.session_state.timeline = None
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "timeline_explanation" not in st.session_state:
    st.session_state.timeline_explanation = None

st.header("📂 Case Tracking")
case_number = st.text_input("Enter Case Number")

# --- Track Case button ---
if st.button("Track Case"):
    with st.spinner("Fetching case details..."):
        st.session_state.case_data = track_case(case_number)
        st.session_state.timeline = get_case_timeline(case_number)

        case_summary = f"""
        Case Number: {st.session_state.case_data['case_number']}
        Court: {st.session_state.case_data['court_name']}
        Status: {st.session_state.case_data['status']}
        Stage: {st.session_state.case_data['stage']}
        Next Hearing: {st.session_state.case_data['next_hearing']}
        """
        st.session_state.explanation = explain_legal_text(
            user_query=case_summary, language=language
        )
        # Reset timeline explanation when tracking a new case
        st.session_state.timeline_explanation = None

# --- Always render case output if data exists in state ---
if st.session_state.case_data:
    case_data = st.session_state.case_data

    st.subheader("Case Information")
    st.write("Case Number:",  case_data["case_number"])
    st.write("Court:",        case_data["court_name"])
    st.write("Status:",       case_data["status"])
    st.write("Stage:",        case_data["stage"])
    st.write("Next Hearing:", case_data["next_hearing"])

    st.divider()
    st.subheader("AI Explanation")
    st.markdown(st.session_state.explanation["response"])

    st.divider()
    st.subheader("📅 Case Timeline")

    for event in st.session_state.timeline:
        st.markdown(f"**{event.event_date}** — {event.event_title}\n\n{event.event_description}")

    st.divider()

    # --- Explain Timeline button ---
    if st.button("Explain Timeline"):
        if not case_number:
            st.warning("Please enter a case number first.")
        else:
            with st.spinner("Analyzing timeline..."):
                result = explain_timeline(case_number, language)
                st.session_state.timeline_explanation = result["response"]

    # Always render timeline explanation if it exists
    if st.session_state.timeline_explanation:
        st.subheader("📖 Timeline Explanation")
        st.markdown(st.session_state.timeline_explanation)