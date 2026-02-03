import streamlit as st
import time
import importlib.util
from pathlib import Path

# --------------------------------------------------
# LOAD LIFE LOOP
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

life_loop_mod = load_module(
    "life_loop",
    ROOT / "00_CORE_EXISTENCE/bootstrap/life_loop.py"
)

LifeLoop = life_loop_mod.LifeLoop

# --------------------------------------------------
# STREAMLIT SETUP
# --------------------------------------------------
st.set_page_config(
    page_title="A7DO — Live Introspection Dashboard",
    layout="wide"
)

st.title("🧠 A7DO — Live Introspection Dashboard")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "life" not in st.session_state:
    st.session_state.life = LifeLoop()

if "history" not in st.session_state:
    st.session_state.history = {
        "energy": [],
        "fatigue": [],
        "time": [],
    }

life = st.session_state.life

# --------------------------------------------------
# CONTROLS
# --------------------------------------------------
col_a, col_b, col_c = st.columns(3)

with col_a:
    auto_run = st.checkbox("Auto run", value=True)

with col_b:
    step = st.button("Single tick")

with col_c:
    delay = st.slider("Tick delay (s)", 0.01, 1.0, 0.1)

# --------------------------------------------------
# ADVANCE LIFE
# --------------------------------------------------
if step or auto_run:
    life.tick()

    snap = life.snapshot()

    st.session_state.history["energy"].append(snap["energy"]["energy"])
    st.session_state.history["fatigue"].append(snap["fatigue"])
    st.session_state.history["time"].append(len(st.session_state.history["time"]))

    if auto_run:
        time.sleep(delay)
        st.rerun()

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------
left, right = st.columns([2, 1])

# --------------------------------------------------
# LEFT — STATE + CHARTS
# --------------------------------------------------
with left:
    st.subheader("🌍 World / Body State")
    st.json(life.world.snapshot())

    st.subheader("⚡ Energy & Fatigue Over Time")
    st.line_chart({
        "energy": st.session_state.history["energy"],
        "fatigue": st.session_state.history["fatigue"],
    })

# --------------------------------------------------
# RIGHT — STATUS + MEMORY
# --------------------------------------------------
with right:
    snap = life.snapshot()

    st.subheader("❤️ Vital Status")
    st.metric("Alive", snap["alive"])
    st.metric("Sleep state", "Awake" if snap["awake"] else "Asleep")

    st.subheader("🕒 Time")
    st.write({
        "internal_time": life.internal_time,
        "world_time": life.world_time.t,
    })

    st.subheader("🧠 Recent Memory")
    memories = life.recent_memory(5)
    if memories:
        for m in memories:
            st.json(m)
    else:
        st.write("No memory yet.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption("A7DO — physics-governed, time-aware, embodied system")
