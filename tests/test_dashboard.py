import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_dashboard_renders_snapshot_text():
    dash = load(
        ROOT / "12_INTERFACE_AND_OBSERVABILITY/dashboard.py",
        "dashboard"
    )
    snap = load(
        ROOT / "12_INTERFACE_AND_OBSERVABILITY/snapshot.py",
        "snapshot"
    )
    world = load(
        ROOT / "09_WORLD_MODEL/world_state.py",
        "world"
    )
    pred = load(
        ROOT / "09_WORLD_MODEL/prediction.py",
        "prediction"
    )
    mem = load(
        ROOT / "07_MEMORY_SYSTEM/episodic.py",
        "memory"
    )
    att = load(
        ROOT / "06_LIMBIC_AND_VALUE_SYSTEM/attention.py",
        "attention"
    )
    council = load(
        ROOT / "10_MULTI_AGENT_COUNCIL/council.py",
        "council"
    )

    World = world.WorldState
    Memory = mem.EpisodicMemory
    Attention = att.AttentionSystem
    Predictor = pred.Predictor
    Council = council.Council
    Snapshot = snap.IntrospectionSnapshot
    Dashboard = dash.Dashboard

    w = World()
    m = Memory(capacity=10)
    a = Attention(m, focus_size=3)
    p = Predictor(w, m)
    c = Council(w, m, p, a)

    m.record({"type": "pain_withdrawal", "strain": 0.9}, salience=0.8)
    w.update(energy=4.0, strain=0.7)

    s = Snapshot(w, m, a, p, c)
    d = Dashboard(s)

    output = d.render_text()

    assert isinstance(output, str)
    assert "WORLD" in output
    assert "MEMORY" in output
    assert "ATTENTION" in output
    assert "PREDICTION" in output
    assert "COUNCIL" in output
