import streamlit as st
import time


class WebDashboard:
    """
    Read-only Streamlit dashboard.
    Displays live introspection snapshots and evidence.
    """

    def __init__(self, snapshot, ledger=None, refresh_seconds: float = 1.0):
        self.snapshot = snapshot
        self.ledger = ledger
        self.refresh_seconds = refresh_seconds

    def run(self):
        st.set_page_config(page_title="A7DO Dashboard", layout="wide")
        st.title("🧠 A7DO — Live Introspection Dashboard")

        placeholder = st.empty()

        while True:
            view = self.snapshot.capture()

            with placeholder.container():
                col1, col2 = st.columns(2)

                # -----------------------------
                # LEFT COLUMN
                # -----------------------------
                with col1:
                    st.subheader("🌍 World State")
                    st.json(view.get("world", {}))

                    st.subheader("🔮 Prediction")
                    st.json(view.get("prediction", {}))

                    # -----------------------------
                    # Evidence + Plots
                    # -----------------------------
                    if self.ledger is not None:
                        st.subheader("📊 Evidence (Recent)")
                        events = self.ledger.recent(50)

                        if not events:
                            st.write("No evidence recorded yet.")
                        else:
                            # Extract series
                            times = [e["time"] for e in events]
                            errors = [
                                e["error"] for e in events
                                if e["error"] is not None
                            ]
                            confidences = [
                                e["confidence"] for e in events
                                if e["error"] is not None
                            ]

                            # Table view (compact)
                            st.dataframe(
                                [
                                    {
                                        "time": e["time"],
                                        "expected": e["prediction"].get("expected_strain"),
                                        "observed": e["outcome"].get("strain"),
                                        "error": e["error"],
                                        "confidence": e["confidence"],
                                    }
                                    for e in events
                                ],
                                use_container_width=True,
                            )

                            # Plot: Error vs Time
                            if errors:
                                st.subheader("📈 Error vs Time")
                                st.line_chart(
                                    {
                                        "error": errors
                                    }
                                )

                            # Plot: Confidence vs Error
                            if errors and confidences:
                                st.subheader("🎯 Confidence vs Error")
                                st.scatter_chart(
                                    {
                                        "confidence": confidences,
                                        "error": errors,
                                    }
                                )

                # -----------------------------
                # RIGHT COLUMN
                # -----------------------------
                with col2:
                    st.subheader("🧠 Attention")
                    st.json(view.get("attention", []))

                    st.subheader("🏛️ Council")
                    st.json(view.get("council", {}))

                st.subheader("📚 Recent Memory")
                st.json(view.get("memory", []))

            time.sleep(self.refresh_seconds)
