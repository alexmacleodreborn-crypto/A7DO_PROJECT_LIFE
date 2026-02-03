import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_modules():
    world_path = ROOT / "09_WORLD_MODEL/world_state.py"
    pred_path = ROOT / "09_WORLD_MODEL/prediction.py"
    mem_path = ROOT / "07_MEMORY_SYSTEM/episodic.py"

    w_spec = importlib.util.spec_from_file_location("world_state", world_path)
    w_mod = importlib.util.module_from_spec(w_spec)
    w_spec.loader.exec_module(w_mod)

    p_spec = importlib.util.spec_from_file_location("prediction", pred_path)
    p_mod = importlib.util.module_from_spec(p_spec)
    p_spec.loader.exec_module(p_mod)

    m_spec = importlib.util.spec_from_file_location("episodic", mem_path)
    m_mod = importlib.util.module_from_spec(m_spec)
    m_spec.loader.exec_module(m_mod)

    return w_mod.WorldState, p_mod.Predictor, m_mod.EpisodicMemory


def test_prediction_reports_expected_strain_increase():
    WorldState, Predictor, Memory = load_modules()

    world = WorldState()
    memory = Memory(capacity=10)

    # Past experience: high strain follows withdrawal
    memory.record(
        {"type": "pain_withdrawal", "strain": 0.9},
        salience=0.8
    )

    world.update(
        energy=4.0,
        strain=0.6,
        last_action="withdraw_limb"
    )

    predictor = Predictor(world, memory)
    forecast = predictor.predict()

    assert forecast["expected_strain"] >= 0.6
    assert forecast["confidence"] > 0.0


def test_prediction_is_read_only():
    WorldState, Predictor, Memory = load_modules()

    world = WorldState()
    memory = Memory(capacity=10)

    world.update(energy=5.0, strain=0.2)
    snapshot_before = world.snapshot()

    predictor = Predictor(world, memory)
    _ = predictor.predict()

    snapshot_after = world.snapshot()

    assert snapshot_before == snapshot_after, "Prediction must not mutate world state"
