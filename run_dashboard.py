"""
A7DO Web Dashboard Runner
Read-only observability + evidence wiring
"""

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

# Interface / Observability
visual_mod = load(
    ROOT / "12_INTERFACE_AND_OBSERVABILITY/visualisation.py",
    "visualisation"
)
snapshot_mod = load(
    ROOT / "12_INTERFACE_AND_OBSERVABILITY/snapshot.py",
    "snapshot"
)
logging_mod = load(
    ROOT / "12_INTERFACE_AND_OBSERVABILITY/logging.py",
    "logging"
)

# World + Cognition
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
attention_mod = load(
    ROOT / "06_LIMBIC_AND_VALUE_SYSTEM/attention.py",
    "attention"
)
council_mod = load(
    ROOT / "10_MULTI_AGENT_COUNCIL/council.py",
    "council"
)

# Evidence Ledger
ledger_mod = load(
    ROOT / "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/evidence_ledger.py",
    "ledger"
)

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
WebDashboard = visual_mod.WebDashboard
IntrospectionSnapshot = snapshot_mod.IntrospectionSnapshot
EvidenceLogger = logging_mod.EvidenceLogger
EvidenceLedger = ledger_mod.EvidenceLedger

WorldState = world_mod.WorldState
EpisodicMemory = memory_mod.EpisodicMemory
AttentionSystem = attention_mod.AttentionSystem
Predictor = prediction_mod.Predictor
Council = council_mod.Council

# --------------------------------------------------
# BUILD SYSTEM (OBSERVATION ONLY)
# --------------------------------------------------
def build_system():
    # Core state
    world = WorldState()
    memory = EpisodicMemory(capacity=20)
    attention = AttentionSystem(memory, focus_size=5)
    predictor = Predictor(world, memory)
    council = Council(world, memory, predictor, attention)

    # Evidence
    ledger = EvidenceLedger()
    logger = EvidenceLogger(ledger)

    # Seed initial experience (for visibility)
    memory.record(
        {"type": "pain_withdrawal", "strain": 0.9},
        salience=0.8
    )

    world.update(
        energy=4.0,
        strain=0.7,
        last_action="withdraw_limb"
    )

    # Initial prediction → evidence
    prediction = predictor.predict()
    logger.observe_prediction(
        world_snapshot=world.snapshot(),
        prediction=prediction
    )
    logger.observe_outcome(
        world_snapshot=world.snapshot(),
        confidence=prediction.get("confidence", 0.0),
        notes="initial dashboard observation"
    )

    snapshot = IntrospectionSnapshot(
        world,
        memory,
        attention,
        predictor,
        council
    )

    return snapshot, ledger

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    snapshot, ledger = build_system()
    WebDashboard(snapshot, ledger=ledger).run()

