"""
frontend/components/captcha_display.py - CAPTCHA Display
"""

import streamlit as st
import os
from PIL import Image
from utils.constants import CAPTCHA_IMAGE_PATH

def render_captcha_display():
    """Render CAPTCHA display."""
    st.subheader("🔐 CAPTCHA Required")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if os.path.exists(CAPTCHA_IMAGE_PATH):
            try:
                img = Image.open(CAPTCHA_IMAGE_PATH)
                st.image(img, caption="Enter the characters shown above", use_container_width=True)
            except:
                st.warning("Check captcha_temp.png in your project folder")
        else:
            st.warning("No CAPTCHA image found. Try searching again.")
    
    with col2:
        st.caption("💡 Open 'captcha_temp.png' in your project folder")
        
        captcha_input = st.text_input(
            "CAPTCHA Answer",
            placeholder="Type characters you see",
            key="captcha_input_ui",
            help="Case insensitive"
        )
        
        if st.button("✅ Submit & Retry", type="primary", width="stretch"):
            if captcha_input:
                st.session_state.captcha_answer = captcha_input.lower()
                st.session_state.show_captcha = False
                st.rerun()
                return True
            else:
                st.error("Please enter the CAPTCHA")
    
    return False