"""
Measure phase lag between predicted and observed strain
using cross-correlation.
"""

import json
import numpy as np
from pathlib import Path

LEDGER_PATH = Path(
    "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/evidence.jsonl"
)

def load_series():
    expected = []
    observed = []

    with open(LEDGER_PATH, "r") as f:
        for line in f:
            e = json.loads(line)
            exp = e["prediction"].get("expected_strain")
            obs = e["outcome"].get("strain")

            if exp is not None and obs is not None:
                expected.append(exp)
                observed.append(obs)

    return np.array(expected), np.array(observed)


def compute_lag(expected, observed):
    """
    Returns lag in timesteps.
    Positive lag means prediction lags behind reality.
    """
    expected = expected - expected.mean()
    observed = observed - observed.mean()

    corr = np.correlate(observed, expected, mode="full")
    lag_index = corr.argmax() - (len(expected) - 1)

    return lag_index


if __name__ == "__main__":
    expected, observed = load_series()

    if len(expected) < 10:
        print("Not enough data to measure lag.")
    else:
        lag = compute_lag(expected, observed)
        print("=" * 50)
        print(f"Measured phase lag: {lag} timesteps")
        print("=" * 50)
