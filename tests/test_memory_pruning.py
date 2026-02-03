import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_memory():
    path = ROOT / "07_MEMORY_SYSTEM/episodic.py"
    spec = importlib.util.spec_from_file_location("episodic", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EpisodicMemory

def test_memory_prunes_when_capacity_exceeded():
    Memory = load_memory()
    mem = Memory(capacity=3)

    mem.record({"type": "a"}, salience=0.1)
    mem.record({"type": "b"}, salience=0.2)
    mem.record({"type": "c"}, salience=0.3)
    mem.record({"type": "d"}, salience=0.9)  # exceeds capacity

    events = [m["event"]["type"] for m in mem.recent(10)]

    assert "a" not in events, "Lowest salience memory should be pruned"
    assert "d" in events, "High salience memory should survive"

def test_salience_decays_over_time():
    Memory = load_memory()
    mem = Memory(capacity=10, decay_rate=0.1)

    mem.record({"type": "x"}, salience=1.0)
    mem.tick()  # decay once

    s = mem._events[0]["salience"]
    assert s < 1.0, "Salience should decay over time"
