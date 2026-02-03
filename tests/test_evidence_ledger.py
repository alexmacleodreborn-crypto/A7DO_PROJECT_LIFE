import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_ledger():
    path = ROOT / "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/evidence_ledger.py"
    spec = importlib.util.spec_from_file_location("evidence_ledger", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EvidenceLedger


def test_evidence_ledger_records_prediction_vs_outcome():
    EvidenceLedger = load_ledger()
    ledger = EvidenceLedger()

    world = {"energy": 4.0, "strain": 0.6}
    prediction = {"expected_strain": 0.9}
    outcome = {"strain": 0.7}
    confidence = 0.25

    event = ledger.record(
        world=world,
        prediction=prediction,
        outcome=outcome,
        confidence=confidence,
        notes="test event",
    )

    # Ledger length
    assert len(ledger.all()) == 1

    # Stored fields
    assert event["world"] == world
    assert event["prediction"] == prediction
    assert event["outcome"] == outcome
    assert event["confidence"] == confidence

    # Error calculation
    assert event["error"] == abs(0.9 - 0.7)

    # Append-only behavior
    ledger.record(
        world=world,
        prediction=prediction,
        outcome={"strain": 0.9},
        confidence=0.9,
    )

    assert len(ledger.all()) == 2
    assert ledger.recent(1)[0]["outcome"]["strain"] == 0.9
