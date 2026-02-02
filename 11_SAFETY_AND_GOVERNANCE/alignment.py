# alignment.py

class AlignmentMonitor:
    """
    Monitors long-term goal alignment.
    """

    def __init__(self):
        self.drift_score = 0.0

    def update(self, signal: float):
        self.drift_score += signal

    def aligned(self) -> bool:
        return self.drift_score < 1.0
