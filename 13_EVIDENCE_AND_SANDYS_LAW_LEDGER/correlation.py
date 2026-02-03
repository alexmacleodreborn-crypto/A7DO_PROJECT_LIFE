import json
from pathlib import Path
from time import time

LEDGER = Path(
    "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/evidence.jsonl"
)

def append_evidence(world, prediction):
    record = {
        "time": time(),
        "prediction": prediction,
        "outcome": {
            "strain": world["strain"],
            "energy": world["energy"],
        },
        "error": abs(prediction["expected_strain"] - world["strain"]),
        "confidence": prediction["confidence"],
    }

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(record) + "\n")

    return record
