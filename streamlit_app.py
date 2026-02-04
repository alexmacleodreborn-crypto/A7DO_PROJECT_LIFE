"""
A7DO — Mobile Streamlit Entry Point

This filE exists ONLY to host and route
the existing dashboards in a mobile-friendly way.

It does NOT create state.
It does NOT create LifeLoop.
"""

import streamlit as st

# --------------------------------------------------
# PAGE CONFIG (MOBILE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="A7DO",
    page_icon="🧠",
    layout="centered",  # better for phone
    initial_sidebar_state="collapsed",
)

st.title("🧠 A7DO")

st.caption("Embodied, physics-governed cognitive system")

# --------------------------------------------------
# SIMPLE NAVIGATION
# --------------------------------------------------
page = st.radio(
    "View",
    [
        "Live Introspection",
        "About",
    ],
    horizontal=False,
)

st.divider()

# --------------------------------------------------
# ROUTING
# --------------------------------------------------
if page == "Live Introspection":
    # Import and run the existing dashboard
    import run_dashboard  # noqa: F401

elif page == "About":
    st.markdown(
        """
        ### A7DO

        A7DO is an embodied, time-aware cognitive system governed by
        physical constraints (Sandy’s Law).

        **Capabilities**
        - Energy-based survival
        - Sleep / wake cycles
        - Fatigue & recovery
        - Episodic memory
        - Prediction & evidence logging
        - Multi-timescale clocks

        **Status**
        - Core life loop: ✅
        - Physics integration: ✅
        - Memory: ✅
        - Prediction: active (uncalibrated)
        - Learning: pending

        This interface is read-only.
        """
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("A7DO — one organism, one physics, one timeline")