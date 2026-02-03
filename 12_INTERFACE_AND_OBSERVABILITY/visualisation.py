import streamlit as st
import time


class WebDashboard:
    """
    Read-only Streamlit dashboard.
    Displays live introspection snapshots.
    """

    def __init__(self, snapshot, refresh_seconds: float = 1.0):
        self.snapshot = snapshot
        self.refresh_seconds = refresh_seconds

    def run(self):
        st.set_page_config(page_title="A7DO Dashboard", layout="wide")
        st.title("🧠 A7DO — Live Introspection Dashboard")

        placeholder = st.empty()

        while True:
            view = self.snapshot.capture()

            with placeholder.container():
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🌍 World State")
                    st.json(view.get("world", {}))

                    st.subheader("🔮 Prediction")
                    st.json(view.get("prediction", {}))

                with col2:
                    st.subheader("🧠 Attention")
                    st.json(view.get("attention", []))

                    st.subheader("🏛️ Council")
                    st.json(view.get("council", {}))

                st.subheader("📚 Recent Memory")
                st.json(view.get("memory", []))

            time.sleep(self.refresh_seconds)
