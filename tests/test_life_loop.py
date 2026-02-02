import importlib.util
from pathlib import Path
import pytest

# --------------------------------------------------
# Load life_loop via file path (numbered folders safe)
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

def load_life_loop():
    path = ROOT / "00_CORE_EXISTENCE/bootstrap/life_loop.py"
    spec = importlib.util.spec_from_file_location("life_loop", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LifeLoop

# --------------------------------------------------
# TESTS
# --------------------------------------------------

def test_withdrawal_without_energy_triggers_shutdown():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    # Drain all energy manually
    life.energy.available = 0.0

    # Force strain high enough to cause pain
    life.overload.strain = 1.0

    life.tick()

    assert not life.pulse.is_alive(), "Life should shut down with no energy"


def test_memory_write_consumes_energy():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    energy_before = life.energy.level()

    life.record_memory(
        event={"type": "test", "time": 0.0},
        salience=0.5
    )

    energy_after = life.energy.level()

    assert energy_after < energy_before, "Memory write must consume energy"


def test_salience_attached_to_memory():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    life.record_memory(
        event={"type": "salience_test", "time": 1.0},
        salience=0.9
    )

    memories = life.memory.recent(1)
    memory = memories[0]

    memory_id = f"{memory['event']['type']}_{memory['time']}"

    assert life.salience.get(memory_id) == 0.9, "Salience must be stored correctly"

def test_proprioception_only_after_motor():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    # Force pain condition
    life.overload.strain = 1.0

    life.tick()

    # Look for proprioception in memory
    memories = life.memory.recent(5)
    found = any(
        m["event"]["type"] == "pain_withdrawal"
        and "body_state" in m["event"]
        for m in memories
    )

    assert found, "Proprioception should be recorded after withdrawal"

def test_physics_gate_blocks_illegal_energy_use():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    # Set energy lower than base cost
    life.energy.available = 0.1

    life.tick()

    assert not life.pulse.is_alive(), "PhysicsGate must enforce shutdown on violation"
