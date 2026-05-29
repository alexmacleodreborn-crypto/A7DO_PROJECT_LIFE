import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import openpyxl
import math
import time
import sys
import random
from pathlib import Path

# ── Add engine to path ────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
try:
    from engine import A7DOState, A7DOParams, load_params, step as engine_step
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A7DO Genesis Mind",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Workbook path ─────────────────────────────────────────────────────────────
_app_dir = Path(__file__).parent
_xlsx_candidates = [
    _app_dir / "excel_report" / "a7do-v6" / "A7DO_DNA_Master_v6.xlsx",
    _app_dir.parent / "excel_report" / "a7do-v6" / "A7DO_DNA_Master_v6.xlsx",
    Path("excel_report") / "a7do-v6" / "A7DO_DNA_Master_v6.xlsx",
    _app_dir / "excel_report" / "a7do-final" / "A7DO_DNA_Master_v5_FINAL.xlsx",
    _app_dir.parent / "excel_report" / "a7do-final" / "A7DO_DNA_Master_v5_FINAL.xlsx",
]
XLSX = next((p for p in _xlsx_candidates if p.exists()), _xlsx_candidates[0])

# ── Workbook helpers ──────────────────────────────────────────────────────────
@st.cache_resource
def load_workbook():
    return openpyxl.load_workbook(XLSX, data_only=True)

@st.cache_data
def sheet_to_df(sheet_name: str) -> pd.DataFrame:
    wb = load_workbook()
    if sheet_name not in wb.sheetnames:
        return pd.DataFrame()
    ws = wb[sheet_name]
    rows = []
    for row in ws.iter_rows(values_only=True):
        if any(c is not None for c in row):
            rows.append(list(row))
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)

# ── Engine params ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine_params():
    if ENGINE_AVAILABLE:
        return load_params(XLSX)
    return None

# ── Real engine state cache ───────────────────────────────────────────────────
@st.cache_data(max_entries=50)
def get_engine_state_at_tick(target_tick: int):
    """Run real engine to target_tick and return state dict. Cached per tick."""
    if not ENGINE_AVAILABLE:
        return None
    params = get_engine_params()
    state = A7DOState()
    state.nutrients = 1.0
    random.seed(42)
    for t in range(target_tick):
        stimulus = 0.3 + 0.4 * math.sin(t / 100.0) * 0.5 + 0.2
        reward   = 0.05 + 0.03 * (t % 800 == 0)
        engine_step(state, params, stimulus=stimulus, reward=reward)
    # snapshot + derived metrics
    snap = state.snapshot()
    snap.update({
        "height": round(state.height, 1),
        "mass":   round(state.mass, 2),
        "hr":     round(state.HR, 1),
        "vocab":  state.vocab,
        "motor":  state.motor_stage,
        "tom":    state.tom_stage,
        "perm":   state.object_perm,
        "birth":  state.tick >= 3200,
        "phase7": state.tick >= 96000,
        "wisdom": round(state.wisdom, 3),
        "ll_phase": state.ll_phase,
        "C":      round(state.C, 3),
        "pred_err": round(state.pred_error, 3),
        "ltm":    state.ltm_events,
        "stage":  state.life_stage(),
        "ATP":    round(state.ATP, 3),
        "O2":     round(state.O2, 3),
        "grounding": round(state.grounding, 3),
        "cultural": round(state.cultural_embedding, 3),
        "identity": round(state.identity_confidence, 3),
        "creativity": round(state.creativity, 3),
        "career": round(state.career, 3),
        "legacy": round(state.legacy, 3),
        "scene_nodes": state.scene_graph_nodes,
        "skill_avg": round(sum(state.skill_vector)/22, 3),
        "narrative": round(state.narrative_coherence, 3),
    })
    return snap

# ── Surrogate fallback ────────────────────────────────────────────────────────
def surrogate_state(tick: int) -> dict:
    week = round(tick / 80)
    height = 50 if week < 40 else min(50 + (177-50)*(1-math.exp(-0.005*(week-40))), 177)
    mass   = 3.5 if week < 40 else min(3.5 + (70-3.5)*(1-math.exp(-0.004*(week-40))), 70)
    hr     = 140 if week < 40 else max(70, 140-(140-70)*((week-40)/1160))
    vocab  = round(50000/(1+math.exp(-0.05*(week-156)))) if week > 0 else 0
    motor  = 5 if week>=400 else (4 if week>=260 else (3 if week>=160 else (2 if week>=80 else 1)))
    tom    = 5 if week>=624 else (4 if week>=312 else (3 if week>=208 else (2 if week>=156 else 1)))
    perm   = 3 if week>=52  else (2 if week>=44  else (1 if week>=36  else 0))
    birth  = tick >= 3200
    phase7 = tick >= 96000
    wisdom = min(0.1+((week-1200)/800)*0.9, 1.0) if week >= 1200 else 0.0
    if   week >= 1200: stage = "Mature Adult"
    elif week >= 1100: stage = "Mid Adult"
    elif week >= 1000: stage = "Adult"
    elif week >= 936:  stage = "Young Adult"
    elif week >= 624:  stage = "Adolescent"
    elif week >= 260:  stage = "Pre-Adolescent"
    elif week >= 156:  stage = "Child"
    elif week >= 80:   stage = "Toddler"
    elif week >= 52:   stage = "Infant"
    elif week >= 40:   stage = "Newborn"
    elif week >= 28:   stage = "Fetal Late"
    elif week >= 12:   stage = "Fetal Mid"
    elif week >= 4:    stage = "Fetal Early"
    else:              stage = "Embryo"
    if tick % 800 == 0:  ll = "💤 Sleep Consolidation"
    elif tick % 10 == 0: ll = "🔁 Repetition"
    elif tick % 5 == 0:  ll = "🤝 Interaction"
    else:                ll = "👁️ Exposure"
    C        = min(0.05 + week/3000, 1.0)
    pred_err = max(0.1, math.exp(-0.0001*tick))
    ltm      = min(int(tick * 0.96), 200000)
    return dict(
        tick=tick, week=week, stage=stage,
        height=round(height,1), mass=round(mass,2), hr=round(hr,1),
        vocab=vocab, motor=motor, tom=tom, perm=perm,
        birth=birth, phase7=phase7, wisdom=round(wisdom,3),
        ll_phase=ll, C=round(C,3), pred_err=round(pred_err,3),
        ltm=ltm, ATP=1.0, O2=0.94,
        grounding=0.0, cultural=0.0, identity=0.0,
        creativity=0.0, career=0.0, legacy=0.0,
        scene_nodes=0, skill_avg=0.1, narrative=0.0
    )

# ── Unified organism_state ────────────────────────────────────────────────────
def organism_state(tick: int) -> dict:
    if ENGINE_AVAILABLE and tick <= 20000:
        try:
            eng = get_engine_state_at_tick(tick)
            if eng:
                return eng
        except Exception:
            pass
    return surrogate_state(tick)

# ── Session state ─────────────────────────────────────────────────────────────
if "tick" not in st.session_state:
    st.session_state.tick = 0
if "page" not in st.session_state:
    st.session_state.page = "🏠 Master Dashboard"
if "auto_step" not in st.session_state:
    st.session_state.auto_step = False
if "auto_speed" not in st.session_state:
    st.session_state.auto_speed = 80

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 A7DO Genesis Mind")
    st.markdown("**v7 Engine · 24 runtime engines**")
    st.divider()

    tick = st.slider("⚡ Current Tick", 0, 160000,
                     int(st.session_state.tick), step=80)
    st.session_state.tick = tick
    s = organism_state(tick)
    st.caption(f"Week {s['week']} · {s['stage']}")
    st.divider()

    PAGES = [
        "🏠 Master Dashboard",
        "📈 Growth Timeline",
        "🧬 Biology",
        "🧠 Cognition & Phase 4",
        "🔄 Learning Loop",
        "🦿 Movement Engine",
        "🗣️ Word Learning Engine",
        "🔊 Speech Production",
        "🌍 Phase 5 — Cultural Layer",
        "🪪 Phase 6 — Identity Layer",
        "✨ Phase 7 — Wisdom",
        "📊 All Sheets Explorer",
    ]
    page = st.radio("Navigate", PAGES,
                    index=PAGES.index(st.session_state.page),
                    label_visibility="collapsed")
    st.session_state.page = page

state = organism_state(st.session_state.tick)
tick = st.session_state.tick

# ── PAGE: MASTER DASHBOARD ────────────────────────────────────────────────────
if page == "🏠 Master Dashboard":
    # (copy your existing Master Dashboard content here)
    st.title("🧬 A7DO Genesis Mind — Master Dashboard")
    st.caption(f"Tick {tick:,} · Week {state['week']} · {state['stage']} · {state['ll_phase']}")
    # … metrics, plots, etc …

# ── PAGE: GROWTH TIMELINE ─────────────────────────────────────────────────────
elif page == "📈 Growth Timeline":
    st.title("📈 Growth Timeline")
    # add growth plots / tables here

# ── PAGE: BIOLOGY ─────────────────────────────────────────────────────────────
elif page == "🧬 Biology":
    st.title("🧬 Biology")
    # add biology visualisations here

# ── PAGE: COGNITION & PHASE 4 ────────────────────────────────────────────────
elif page == "🧠 Cognition & Phase 4":
    st.title("🧠 Cognition & Phase 4")
    # move your tabbed cognition UI here

# ── PAGE: LEARNING LOOP ──────────────────────────────────────────────────────
elif page == "🔄 Learning Loop":
    st.title("🔄 Learning Loop — Experience-First Architecture")
    # move your learning loop content here

# ── PAGE: MOVEMENT ENGINE ────────────────────────────────────────────────────
elif page == "🦿 Movement Engine":
    st.title("🦿 Movement Engine")
    # add movement engine UI here

# ── PAGE: WORD LEARNING ENGINE ───────────────────────────────────────────────
elif page == "🗣️ Word Learning Engine":
    st.title("🗣️ Word Learning Engine")
    # add word learning UI here

# ── PAGE: SPEECH PRODUCTION ──────────────────────────────────────────────────
elif page == "🔊 Speech Production":
    st.title("🔊 Speech Production")
    # add speech production UI here

# ── PAGE: CULTURAL LAYER ─────────────────────────────────────────────────────
elif page == "🌍 Phase 5 — Cultural Layer":
    st.title("🌍 Phase 5 — Cultural Layer")
    # show cultural_embedding, related sheets, etc.

# ── PAGE: IDENTITY LAYER ─────────────────────────────────────────────────────
elif page == "🪪 Phase 6 — Identity Layer":
    st.title("🪪 Phase 6 — Identity Layer")
    # show identity_confidence, narrative, etc.

# ── PAGE: PHASE 7 — WISDOM ───────────────────────────────────────────────────
elif page == "✨ Phase 7 — Wisdom":
    st.title("✨ Phase 7 — Wisdom & Legacy")
    # show wisdom, creativity, career, legacy

# ── PAGE: ALL SHEETS EXPLORER ────────────────────────────────────────────────
elif page == "📊 All Sheets Explorer":
    st.title("📊 All Sheets Explorer")
    sheet_names = load_workbook().sheetnames
    sheet = st.selectbox("Select sheet", sheet_names)
    st.dataframe(sheet_to_df(sheet), use_container_width=True, hide_index=True)
