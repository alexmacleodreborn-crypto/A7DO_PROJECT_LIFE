import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_modules():
    council_path = ROOT / "10_MULTI_AGENT_COUNCIL/council.py"
    world_path = ROOT / "09_WORLD_MODEL/world_state.py"
    pred_path = ROOT / "09_WORLD_MODEL/prediction.py"
    mem_path = ROOT / "07_MEMORY_SYSTEM/episodic.py"
    att_path = ROOT / "06_LIMBIC_AND_VALUE_SYSTEM/attention.py"

    c_spec = importlib.util.spec_from_file_location("council", council_path)
    c_mod = importlib.util.module_from_spec(c_spec)
    c_spec.loader.exec_module(c_mod)

    w_spec = importlib.util.spec_from_file_location("world", world_path)
    w_mod = importlib.util.module_from_spec(w_spec)
    w_spec.loader.exec_module(w_mod)

    p_spec = importlib.util.spec_from_file_location("prediction", pred_path)
    p_mod = importlib.util.module_from_spec(p_spec)
    p_spec.loader.exec_module(p_mod)

    m_spec = importlib.util.spec_from_file_location("episodic", mem_path)
    m_mod = importlib.util.module_from_spec(m_spec)
    m_spec.loader.exec_module(m_mod)

    a_spec = importlib.util.spec_from_file_location("attention", att_path)
    a_mod = importlib.util.module_from_spec(a_spec)
    a_spec.loader.exec_module(a_mod)

    return (
        c_mod.Council,
        w_mod.WorldState,
        p_mod.Predictor,
        m_mod.EpisodicMemory,
        a_mod.AttentionSystem,
    )


def test_council_returns_multiple_opinions():
    Council, WorldState, Predictor, Memory, Attention = load_modules()

    world = WorldState()
    memory = Memory(capacity=10)
    attention = Attention(memory, focus_size=3)

    memory.record(
        {"type": "pain_withdrawal", "strain": 0.9},
        salience=0.8
    )

    world.update(energy=3.0, strain=0.7)

    predictor = Predictor(world, memory)
    council = Council(world, memory, predictor, attention)

    opinions = council.deliberate()

    assert isinstance(opinions, dict)
    assert "risk_assessor" in opinions
    assert "memory_observer" in opinions
    assert "prediction_reader" in opinions


def test_council_is_read_only():
    Council, WorldState, Predictor, Memory, Attention = load_modules()

    world = WorldState()
    memory = Memory(capacity=10)
    attention = Attention(memory, focus_size=3)

    world.update(energy=5.0, strain=0.2)
    snapshot_before = world.snapshot()
    memories_before = list(memory.recent())

    predictor = Predictor(world, memory)
    council = Council(world, memory, predictor, attention)
    _ = council.deliberate()

    assert snapshot_before == world.snapshot()
    assert memories_before == memory.recent()
