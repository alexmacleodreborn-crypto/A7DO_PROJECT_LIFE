# falsifiability.py

class FalsifiabilityTracker:
    """
    Tracks claims vs evidence.
    """

    def __init__(self):
        self.claims = []
        self.evidence = []

    def add_claim(self, claim: str):
        self.claims.append(claim)

    def add_evidence(self, evidence: str):
        self.evidence.append(evidence)
