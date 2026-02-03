import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_modules():
    mem_path = ROOT / "07_MEMORY_SYSTEM/episodic.py"
    att_path = ROOT / "06_LIMBIC_AND_VALUE_SYSTEM/attention.py"

    mem_spec = importlib.util.spec_from_file_location("episodic", mem_path)
    mem_mod = importlib.util.module_from_spec(mem_spec)
    mem_spec.loader.exec_module(mem_mod)

    att_spec = importlib.util.spec_from_file_location("attention", att_path)
    att_mod = importlib.util.module_from_spec(att_spec)
    att_spec.loader.exec_module(att_mod)

    return mem_mod.EpisodicMemory, att_mod.AttentionSystem


def test_attention_selects_highest_salience():
    Memory, Attention = load_modules()
    mem = Memory(capacity=10)

    mem.record({"type": "low"}, salience=0.1)
    mem.record({"type": "mid"}, salience=0.5)
    mem.record({"type": "high"}, salience=0.9)

    att = Attention(mem, focus_size=2)
    focus = att.focus()

    types = [m["event"]["type"] for m in focus]

    assert "high" in types
    assert "mid" in types
    assert "low" not in types


def test_attention_is_read_only():
    Memory, Attention = load_modules()
    mem = Memory(capacity=5)

    mem.record({"type": "x"}, salience=0.8)
    before = list(mem.recent())

    att = Attention(mem, focus_size=1)
    _ = att.focus()

    after = list(mem.recent())

    assert before == after, "Attention must not mutate memory"
