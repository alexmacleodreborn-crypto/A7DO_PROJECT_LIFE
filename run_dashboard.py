"""
A7DO — Live Introspection Dashboard
Organism + Prediction + Evidence + Visuals
"""

import streamlit as st
import time
import importlib.util
from pathlib import Path
import json

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# LOAD CORE
# --------------------------------------------------
life_mod = load_module(
    "life_loop",
    "00_CORE_EXISTENCE/bootstrap/life_loop.py"
)
LifeLoop = life_mod.LifeLoop

world_time_mod = load_module("world_time", "09_WORLD_MODEL/time.py")
world_state_mod = load_module("world_state", "09_WORLD_MODEL/world_state.py")
prediction_mod = load_module("prediction", "09_WORLD_MODEL/prediction.py")
evidence_mod = load_module(
    "evidence",
    "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/correlation.py"
)

WorldTime = world_time_mod.WorldTime
WorldState = world_state_mod.WorldState
Predictor = prediction_mod.Predictor
append_evidence = evidence_mod.append_evidence

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "life" not in st.session_state:
    st.session_state.life = LifeLoop(WorldTime(), WorldState())

if "predictor" not in st.session_state:
    st.session_state.predictor = Predictor(horizon=2)

life = st.session_state.life
predictor = st.session_state.predictor

# --------------------------------------------------
# CONTROLS
# --------------------------------------------------
st.sidebar.title("🧠 A7DO Control")

if st.sidebar.button("🔘 Tick"):
    life.tick()

if st.sidebar.button("▶️ Tick + Predict + Log"):
    life.tick()
    prediction = predictor.predict(
        life.world.snapshot(),
        life.memory.recent(5)
    )
    append_evidence(life.world.snapshot(), prediction)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
st.title("🧠 A7DO — Live Introspection Dashboard")

st.subheader("🌍 World / Body State")
st.json(life.world.snapshot())

st.subheader("🔮 Prediction")
st.json(predictor.last_prediction)

st.subheader("🧠 Recent Memory")
st.json(life.memory.recent(5))

# --------------------------------------------------
# EVIDENCE TABLE
# --------------------------------------------------
st.subheader("📊 Evidence (Recent)")

ledger_path = Path(
    "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/evidence.jsonl"
)

rows = []
if ledger_path.exists():
    with open(ledger_path) as f:
        for line in f.readlines()[-10:]:
            rows.append(json.loads(line))

if rows:
    st.dataframe(rows)

st.subheader("❤️ Pulse")
st.write("Alive:", life.pulse.is_alive())
