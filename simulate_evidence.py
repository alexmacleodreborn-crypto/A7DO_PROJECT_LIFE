
import time
import random
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# --------------------------------------------------
# LOAD MODULES
# --------------------------------------------------
world_mod = load(ROOT / "09_WORLD_MODEL/world_state.py", "world")
pred_mod = load(ROOT / "09_WORLD_MODEL/prediction.py", "prediction")
ledger_mod = load(ROOT / "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/evidence_ledger.py", "ledger")
logger_mod = load(ROOT / "12_INTERFACE_AND_OBSERVABILITY/logging.py", "logging")
memory_mod = load(ROOT / "07_MEMORY_SYSTEM/episodic.py", "memory")

WorldState = world_mod.WorldState
Predictor = pred_mod.Predictor
EvidenceLedger = ledger_mod.EvidenceLedger
EvidenceLogger = logger_mod.EvidenceLogger
EpisodicMemory = memory_mod.EpisodicMemory


def run_simulation(steps=50, delay=0.2):
    world = WorldState()
    memory = EpisodicMemory(capacity=50)
    predictor = Predictor(world, memory)

    ledger = EvidenceLedger()
    logger = EvidenceLogger(ledger)

    # Initial conditions
    strain = 0.5
    world.update(energy=5.0, strain=strain)

    for i in range(steps):
        # Seed memory with a synthetic experience
        memory.record(
            {"type": "simulated_state", "strain": strain},
            salience=0.2,
        )

        # Predict
        prediction = predictor.predict()
        logger.observe_prediction(
            world_snapshot=world.snapshot(),
            prediction=prediction,
        )

        # Simulate world drift
        strain += random.uniform(-0.1, 0.15)
        strain = max(0.0, min(1.0, strain))
        world.update(strain=strain)

        # Record outcome
        logger.observe_outcome(
            world_snapshot=world.snapshot(),
            confidence=prediction.get("confidence", 0.0),
            notes=f"sim_step_{i}",
        )

        print(
            f"[{i}] expected={prediction.get('expected_strain')} "
            f"observed={strain:.2f}"
        )

        time.sleep(delay)

    return ledger


if __name__ == "__main__":
    run_simulation()
