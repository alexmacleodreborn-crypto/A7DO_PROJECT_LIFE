import streamlit as st
import time


class WebDashboard:
    """
    Read-only Streamlit dashboard.
    Displays live introspection snapshots, evidence, and calibrated confidence.
    """

    def __init__(
        self,
        snapshot,
        ledger=None,
        calibrator=None,
        refresh_seconds: float = 1.0,
    ):
        self.snapshot = snapshot
        self.ledger = ledger
        self.calibrator = calibrator
        self.refresh_seconds = refresh_seconds

    def run(self):
        st.set_page_config(
            page_title="A7DO — Live Introspection Dashboard",
            layout="wide",
        )
        st.title("🧠 A7DO — Live Introspection Dashboard")

        placeholder = st.empty()

        while True:
            view = self.snapshot.capture()

            with placeholder.container():
                col1, col2 = st.columns(2)

                # ==================================================
                # LEFT COLUMN
                # ==================================================
                with col1:
                    # -----------------------------
                    # World
                    # -----------------------------
                    st.subheader("🌍 World State")
                    st.json(view.get("world", {}))

                    # -----------------------------
                    # Prediction (raw + calibrated)
                    # -----------------------------
                    st.subheader("🔮 Prediction")
                    prediction = view.get("prediction", {})

                    raw_conf = prediction.get("confidence")
                    calibrated_conf = None

                    if (
                        raw_conf is not None
                        and self.calibrator is not None
                        and self.ledger is not None
                    ):
                        calibrated_conf = (
                            self.calibrator.calibrated_confidence(raw_conf)
                        )

                    pred_display = dict(prediction)
                    if calibrated_conf is not None:
                        pred_display["calibrated_confidence"] = calibrated_conf

                    st.json(pred_display)

                    # -----------------------------
                    # Evidence + Plots
                    # -----------------------------
                    if self.ledger is not None:
                        st.subheader("📊 Evidence (Recent)")
                        events = self.ledger.recent(50)

                        if not events:
                            st.write("No evidence recorded yet.")
                        else:
                            # -----------------------------
                            # Table
                            # -----------------------------
                            table = [
                                {
                                    "time": e["time"],
                                    "expected": e["prediction"].get(
                                        "expected_strain"
                                    ),
                                    "observed": e["outcome"].get("strain"),
                                    "error": e["error"],
                                    "confidence": e["confidence"],
                                }
                                for e in events
                            ]
                            st.dataframe(
                                table,
                                use_container_width=True,
                            )

                            # -----------------------------
                            # Extract series
                            # -----------------------------
                            errors = [
                                e["error"]
                                for e in events
                                if e.get("error") is not None
                            ]
                            confidences = [
                                e["confidence"]
                                for e in events
                                if e.get("error") is not None
                            ]

                            # -----------------------------
                            # Error vs Time
                            # -----------------------------
                            if errors:
                                st.subheader("📈 Error vs Time")
                                st.line_chart(
                                    {"error": errors}
                                )

                            # -----------------------------
                            # Confidence vs Error
                            # -----------------------------
                            if errors and confidences:
                                st.subheader("🎯 Confidence vs Error")
                                st.scatter_chart(
                                    {
                                        "confidence": confidences,
                                        "error": errors,
                                    }
                                )

                # ==================================================
                # RIGHT COLUMN
                # ==================================================
                with col2:
                    st.subheader("🧠 Attention")
                    st.json(view.get("attention", []))

                    st.subheader("🏛️ Council")
                    st.json(view.get("council", {}))

                # -----------------------------
                # Memory (full width)
                # -----------------------------
                st.subheader("📚 Recent Memory")
                st.json(view.get("memory", []))

            time.sleep(self.refresh_seconds)
