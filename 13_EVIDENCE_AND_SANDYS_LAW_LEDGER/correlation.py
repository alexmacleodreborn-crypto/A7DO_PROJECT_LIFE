# correlations.py

class CorrelationLedger:
    """
    Tracks correlations between Sandy’s Law predictions
    and empirical observations.
    """

    def __init__(self):
        self.entries = []

    def add(self, claim: str, dataset: str, score: float):
        """
        score ∈ [-1, 1]
        """
        self.entries.append({
            "claim": claim,
            "dataset": dataset,
            "score": score
        })

    def summary(self):
        return list(self.entries)
