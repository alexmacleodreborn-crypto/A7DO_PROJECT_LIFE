"""
Measure phase lag between predicted and observed strain.
Lag is reported relative to the forecast horizon.
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

FORECAST_HORIZON = 2


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
# TRUE LAG COMPUTATION
# --------------------------------------------------
def compute_true_lag(expected, observed, horizon):
    """
    Measures true temporal lag.
    Positive = prediction lags reality
    Negative = prediction leads reality
    """

    n = min(len(expected), len(observed))
    expected = expected[:n] - expected.mean()
    observed = observed[:n] - observed.mean()

    corr = np.correlate(observed, expected, mode="full")
    raw_lag = corr.argmax() - (n - 1)

    # Adjust for forecast horizon
    true_lag = raw_lag - horizon

    return raw_lag, true_lag


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    expected, observed = load_series()

    if expected is None or len(expected) < 20:
        print("Not enough data to measure lag.")
    else:
        raw_lag, true_lag = compute_true_lag(
            expected,
            observed,
            FORECAST_HORIZON,
        )

        print("=" * 60)
        print(f"Forecast horizon: {FORECAST_HORIZON}")
        print(f"Raw correlation lag: {raw_lag}")
        print(f"True lag vs horizon: {true_lag}")
        print("=" * 60)
