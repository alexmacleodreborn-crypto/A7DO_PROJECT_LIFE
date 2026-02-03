class ConfidenceCalibrator:
    """
    Calibrates confidence based on recent prediction error.
    Read-only with respect to cognition.
    """

    def __init__(self, ledger, window: int = 20):
        self.ledger = ledger
        self.window = window

    def calibrated_confidence(self, raw_confidence: float) -> float:
        events = self.ledger.recent(self.window)
        errors = [
            e["error"]
            for e in events
            if e.get("error") is not None
        ]

        if not errors:
            return raw_confidence

        mean_error = sum(errors) / len(errors)

        # Simple, interpretable calibration rule
        calibrated = 1.0 - mean_error

        # Clamp to sane bounds
        calibrated = max(0.05, min(0.95, calibrated))
        return calibrated
