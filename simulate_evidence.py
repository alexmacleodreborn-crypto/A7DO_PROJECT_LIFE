"""
A7DO Structured Evidence Simulation
Deterministic sinusoidal world for falsifiability testing
"""

import time
import math
import importlib.util
from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# --------------------------------------------------
# LOAD MODULES (NUMBERED FOLDERS SAFE)
# --------------------------------------------------
world_mod = load(
    ROOT / "09_WORLD_MODEL/world_state.py",
    "world"
)
prediction_mod = load(
    ROOT / "09_WORLD_MODEL/prediction.py",
    "prediction"
)
memory_mod = load(
    ROOT / "07_MEMORY_SYSTEM/episodic.py",
    "memory"
)
ledger_mod = load(
    ROOT / "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/evidence_ledger.py",
    "ledger"
)
logging_mod = load(
    ROOT / "12_INTERFACE_AND_OBSERVABILITY/logging.py",
    "logging"
)

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
WorldState = world_mod.WorldState
Predictor = prediction_mod.Predictor
EpisodicMemory = memory_mod.EpisodicMemory
EvidenceLedger = ledger_mod.EvidenceLedger
EvidenceLogger = logging_mod.EvidenceLogger

# --------------------------------------------------
# STRUCTURED SIMULATION
# --------------------------------------------------
def run_simulation(
    steps: int = 60,
    delay: float = 0.2,
    amplitude: float = 0.25,
    omega: float = 0.2,
):
    """
    Runs a deterministic sinusoidal world simulation.

    strain(t) = 0.5 + A * sin(omega * t)
    """

    world = WorldState()
    memory = EpisodicMemory(capacity=100)
    predictor = Predictor(world, memory)

    ledger = EvidenceLedger()
    logger = EvidenceLogger(ledger)

    # Initial state
    world.update(
        energy=5.0,
        strain=0.5,
        last_action="structured_sim_start",
    )

    print("▶ Starting structured simulation")
    print("-" * 60)

    for i in range(steps):
        t = i * omega

        # Read current world state safely
        current_world = world.snapshot()
        current_strain = current_world.get("strain")

        # Record prior state into memory
        memory.record(
            {
                "type": "structured_state",
                "strain": current_strain,
                "t": t,
            },
            salience=0.2,
        )

        # Predict
        prediction = predictor.predict()
        logger.observe_prediction(
            world_snapshot=current_world,
            prediction=prediction,
        )

        # Structured world update (sinusoid)
        new_strain = 0.5 + amplitude * math.sin(t)
        new_strain = max(0.0, min(1.0, new_strain))

        world.update(strain=new_strain)

        # Record outcome
        logger.observe_outcome(
            world_snapshot=world.snapshot(),
            confidence=prediction.get("confidence", 0.0),
            notes=f"structured_step_{i}",
        )

        print(
            f"[{i:02d}] "
            f"expected={prediction.get('expected_strain')} "
            f"observed={new_strain:.3f}"
        )

        time.sleep(delay)

    print("-" * 60)
    print("✔ Structured simulation complete")

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    run_simulation()
