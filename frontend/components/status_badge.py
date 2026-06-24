"""
frontend/components/status_badge.py - Status Badge Component
"""

import streamlit as st


def render_status_badge(status: str):
    """Render a status badge with color coding."""

    # Map status to colors
    status_colors = {
        "pending": "#ff4b4b",
        "listed": "#ffa500",
        "in_progress": "#ffa500",
        "disposed": "#00cc66",
        "dismissed": "#808080",
        "institution": "#2196F3",
        "all": "#4a6fa5",
    }

    # Get color or default
    status_lower = status.lower()
    color = status_colors.get(status_lower, "#4a6fa5")

    # Clean status text
    display_status = status if status else "Unknown"

    # Create HTML badge
    badge_html = f"""
    <span style="
    background-color: {color};
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    ">
    {display_status}
    </span>
    """

    st.markdown(badge_html, unsafe_allow_html=True)
