"""
Measure phase lag between predicted and observed strain
accounting for forecast horizon.
"""

import json
import numpy as np
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
LEDGER_PATH = Path(
    "13_EVIDENCE_AND_SANDYS_LAW_LEDGER/datasets/evidence.jsonl"
)

FORECAST_HORIZON = 2  # must match predictor horizon


# --------------------------------------------------
# LOAD SERIES
# --------------------------------------------------
def load_series():
    expected = []
    observed = []

    if not LEDGER_PATH.exists():
        print("Ledger file not found.")
        return None, None

    with open(LEDGER_PATH, "r") as f:
        for line in f:
            e = json.loads(line)

            exp = e.get("prediction", {}).get("expected_strain")
            obs = e.get("outcome", {}).get("strain")

            if exp is not None and obs is not None:
                expected.append(exp)
                observed.append(obs)

    return np.array(expected), np.array(observed)


# --------------------------------------------------
# LAG COMPUTATION (HORIZON-AWARE)
# --------------------------------------------------
def compute_lag(expected, observed, horizon=1):
    """
    Computes lag in timesteps.
    Positive lag means prediction lags reality.
    Negative lag means prediction leads reality.
    """

    if len(expected) <= horizon:
        return None

    # Align prediction(t+h) with observation(t+h)
    expected_aligned = expected[:-horizon]
    observed_aligned = observed[horizon:]

    # Demean
    expected_aligned = expected_aligned - expected_aligned.mean()
    observed_aligned = observed_aligned - observed_aligned.mean()

    # Cross-correlation
    corr = np.correlate(observed_aligned, expected_aligned, mode="full")
    lag_index = corr.argmax() - (len(expected_aligned) - 1)

    return lag_index


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    expected, observed = load_series()

    if expected is None or len(expected) < 10:
        print("Not enough data to measure lag.")
    else:
        lag = compute_lag(
            expected,
            observed,
            horizon=FORECAST_HORIZON,
        )

        print("=" * 60)
        print(f"Forecast horizon: {FORECAST_HORIZON} step(s)")
        print(f"Measured phase lag: {lag} timesteps")
        print("=" * 60)
