"""
A7DO — Live Introspection Dashboard
Manual Tick Control (Authoritative Time Boundary)
"""

import streamlit as st
import time
import importlib.util
from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# LOAD WORLD
# --------------------------------------------------
world_time_mod = load_module("world_time", "09_WORLD_MODEL/time.py")
world_state_mod = load_module("world_state", "09_WORLD_MODEL/world_state.py")

WorldTime = world_time_mod.WorldTime
WorldState = world_state_mod.WorldState

# --------------------------------------------------
# LOAD LIFE LOOP
# --------------------------------------------------
life_loop_mod = load_module(
    "life_loop",
    "00_CORE_EXISTENCE/bootstrap/life_loop.py"
)
LifeLoop = life_loop_mod.LifeLoop

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "life" not in st.session_state:
    world_time = WorldTime()
    world_state = WorldState()
    st.session_state.life = LifeLoop(world_time, world_state)

if "run_ticks_remaining" not in st.session_state:
    st.session_state.run_ticks_remaining = 0

life = st.session_state.life

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.title("🧠 A7DO Control")

if st.sidebar.button("🔘 Tick (1)"):
    life.tick()

run_n = st.sidebar.number_input(
    "Run N ticks",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

if st.sidebar.button("▶️ Run N"):
    st.session_state.run_ticks_remaining = run_n

if st.sidebar.button("⏸ Pause"):
    st.session_state.run_ticks_remaining = 0

# --------------------------------------------------
# RUN LOOP
# --------------------------------------------------
if st.session_state.run_ticks_remaining > 0:
    life.tick()
    st.session_state.run_ticks_remaining -= 1
    time.sleep(0.05)
    st.rerun()

# --------------------------------------------------
# DASHBOARD DISPLAY
# --------------------------------------------------
st.title("🧠 A7DO — Live Introspection Dashboard")

st.subheader("🌍 World / Body State")
st.json({
    "energy": life.energy.level(),
    "strain": life.overload.strain,
    "last_action": getattr(life.motor, "last_action", None),
    "time_internal": life.internal_time,
    "time_real": life.clock.now(),
    "time_world": life.world_time.t,
})

st.subheader("🧠 Recent Memory")
st.json(life.memory.recent(5))

st.subheader("❤️ Pulse")
st.write("Alive:", life.pulse.is_alive())
