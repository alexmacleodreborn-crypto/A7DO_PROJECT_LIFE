import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_world():
    path = ROOT / "09_WORLD_MODEL/world_state.py"
    spec = importlib.util.spec_from_file_location("world_state", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WorldState


def test_world_model_updates_state():
    WorldState = load_world()
    world = WorldState()

    world.update(
        energy=5.0,
        strain=0.8,
        last_action="withdraw_limb"
    )

    snapshot = world.snapshot()

    assert snapshot["energy"] == 5.0
    assert snapshot["strain"] == 0.8
    assert snapshot["last_action"] == "withdraw_limb"


def test_world_model_is_descriptive_only():
    WorldState = load_world()
    world = WorldState()

    world.update(energy=3.0)
    snapshot1 = world.snapshot()

    # Repeated snapshot should not change state
    snapshot2 = world.snapshot()

    assert snapshot1 == snapshot2, "World model must not mutate itself"
