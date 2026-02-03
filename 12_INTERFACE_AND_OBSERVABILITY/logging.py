"""
Observability logging for A7DO.
Wires prediction → outcome into the Evidence Ledger.
Read-only with respect to cognition.
"""

from copy import deepcopy


class EvidenceLogger:
    """
    Observes system state and records evidence events.
    """

    def __init__(self, ledger):
        self.ledger = ledger
        self._last_prediction = None
        self._last_world = None

    def observe_prediction(self, world_snapshot: dict, prediction: dict):
        """
        Capture prediction and world state at time of prediction.
        """
        self._last_world = deepcopy(world_snapshot)
        self._last_prediction = deepcopy(prediction)

    def observe_outcome(
        self,
        world_snapshot: dict,
        confidence: float = 0.0,
        notes: str = "",
    ):
        """
        Compare latest outcome to last prediction and record evidence.
        """
        if self._last_prediction is None or self._last_world is None:
            return None  # Nothing to record yet

        outcome = {
            "strain": world_snapshot.get("strain"),
            "energy": world_snapshot.get("energy"),
        }

        return self.ledger.record(
            world=self._last_world,
            prediction=self._last_prediction,
            outcome=outcome,
            confidence=confidence,
            notes=notes,
        )
