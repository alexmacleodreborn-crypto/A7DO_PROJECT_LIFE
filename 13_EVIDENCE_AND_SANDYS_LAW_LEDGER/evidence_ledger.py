"""
Evidence Ledger for A7DO and Sandy's Law.

This module records raw, append-only evidence events:
prediction → outcome → error.

NO analysis.
NO scoring.
NO mutation of past entries.
"""

import time
from copy import deepcopy


class EvidenceLedger:
    """
    Append-only evidence ledger.
    """

    def __init__(self):
        self._events = []

    def record(
        self,
        *,
        world: dict,
        prediction: dict,
        outcome: dict,
        confidence: float,
        notes: str = "",
    ):
        """
        Record a single evidence event.
        """
        expected = prediction.get("expected_strain")
        observed = outcome.get("strain")

        error = None
        if expected is not None and observed is not None:
            error = abs(observed - expected)

        event = {
            "time": time.time(),
            "world": deepcopy(world),
            "prediction": deepcopy(prediction),
            "outcome": deepcopy(outcome),
            "error": error,
            "confidence": confidence,
            "notes": notes,
        }

        self._events.append(event)
        return event

    def all(self):
        """
        Return all evidence events (read-only copy).
        """
        return list(self._events)

    def recent(self, n: int = 10):
        """
        Return the most recent n evidence events.
        """
        return self._events[-n:]
