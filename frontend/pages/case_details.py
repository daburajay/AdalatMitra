"""
frontend/pages/case_details.py - Complete Case Details with AI Chat
"""

import streamlit as st
from agents.case_summarizer import CaseSummarizer

def render_case_details():
    """Render case details with AI chat."""
    
    case = st.session_state.get("selected_case")
    
    if not case:
        st.warning("No case selected")
        if st.button("← Back to Search"):
            st.session_state.page = "home"
            st.rerun()
        return
    
    # Get case identifier for caching
    case_key = case.get("cnr_number", case.get("case_number", "unknown"))
    
    # Back button
    if st.button("← Back to Results"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("---")
    
    # Case Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1f3a5f 0%, #2d5a87 100%);
        border-radius: 16px;
        padding: 32px;
        color: white;
        margin-bottom: 24px;
    ">
        <div style="font-size: 32px; font-weight: 700;">📋 {case.get('case_number', 'N/A')}</div>
        <div style="font-size: 18px; opacity: 0.9; margin-top: 8px;">{case.get('case_type', 'N/A')} • {case.get('court', 'Delhi High Court')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # AI SUMMARY SECTION - CACHED
    # ============================================================
    st.subheader("🤖 AI Case Summary")
    
    # Get current language
    current_language = st.session_state.get("language", "english")
    lang_name = {
        "english": "English",
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "marathi": "Marathi"
    }.get(current_language, "English")
    
    # Check if we have a cached summary for this case in this language
    cache_key = f"summary_{case_key}_{current_language}"
    
    if cache_key not in st.session_state:
        st.session_state[cache_key] = None
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(f"📝 Generate Summary in {lang_name}", use_container_width=True):
            with st.spinner("🤔 Analyzing case..."):
                summarizer = CaseSummarizer()
                result = summarizer.generate_summary(case, lang_name)
                
                if result.get("success"):
                    st.session_state[cache_key] = {
                        "summary": result.get("summary"),
                        "provider": result.get("provider"),
                        "language": current_language
                    }
                    st.rerun()
                else:
                    st.error(f"❌ {result.get('error', 'Summary generation failed')}")
    
    # Display cached summary if available
    cached = st.session_state.get(cache_key)
    if cached:
        st.markdown(f"""
        <div style="
            background: #f0f4ff;
            border-radius: 12px;
            padding: 20px 24px;
            border-left: 4px solid #1f3a5f;
            margin: 12px 0 20px 0;
        ">
            {cached.get("summary")}
            <div style="margin-top: 8px; font-size: 12px; color: #888;">
                🤖 Generated using {cached.get("provider", "AI")} in {cached.get("language", "English")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # CASE INFORMATION
    # ============================================================
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📌 Case Information")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px;">
            <p><strong>Case Number:</strong> {case.get('case_number', 'N/A')}</p>
            <p><strong>Case Type:</strong> {case.get('case_type', 'N/A')}</p>
            <p><strong>CNR Number:</strong> {case.get('cnr_number', 'N/A')}</p>
            <p><strong>Filing Number:</strong> {case.get('filing_number', 'N/A')}</p>
            <p><strong>Court:</strong> {case.get('court', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 👥 Parties")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px;">
            <p><strong>👤 Petitioner:</strong> {case.get('petitioner', 'N/A')}</p>
            <p><strong>👥 Respondent:</strong> {case.get('respondent', 'N/A')}</p>
            <p><strong>📅 Next Hearing:</strong> {case.get('next_hearing', 'Not scheduled')}</p>
            <p><strong>📋 Status:</strong> {case.get('status', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # AI CHAT SECTION
    # ============================================================
    st.markdown("---")
    st.subheader("💬 Ask AI About This Case")
    
    # Initialize chat history for this case
    chat_key = f"chat_{case_key}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    
    # Display chat history
    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything about this case..."):
        # Add user message
        st.session_state[chat_key].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("💭 Thinking..."):
                try:
                    from services.ai_gateway import AIGateway
                    ai = AIGateway()
                    
                    # Build context from case data
                    context = f"""
Case Details:
- Case Number: {case.get('case_number', 'N/A')}
- Case Type: {case.get('case_type', 'N/A')}
- Status: {case.get('status', 'Pending')}
- Petitioner: {case.get('petitioner', 'N/A')}
- Respondent: {case.get('respondent', 'N/A')}
- Next Hearing: {case.get('next_hearing', 'Not scheduled')}
- CNR: {case.get('cnr_number', 'N/A')}
- Court: {case.get('court', 'Delhi High Court')}
"""
                    
                    chat_prompt = f"""
You are a helpful legal assistant. Answer the user's question based on the case details.
Respond in {lang_name}.

{context}

User Question: {prompt}

Provide a clear, helpful answer. If you don't know something, say so.
Use simple language and avoid legal jargon.
"""
                    
                    response = ai.generate_response(chat_prompt, max_tokens=500)
                    
                    if response.get("success"):
                        answer = response.get("response")
                        st.markdown(answer)
                        st.caption(f"🤖 {response.get('provider', 'AI')}")
                        
                        # Save assistant message
                        st.session_state[chat_key].append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"❌ {response.get('response', 'Failed to generate response')}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Clear chat button
    if st.session_state[chat_key]:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state[chat_key] = []
            st.rerun()