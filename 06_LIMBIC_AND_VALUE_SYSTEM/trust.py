# trust.py

class TrustModel:
    """
    Tracks trust toward external entities.
    """

    def __init__(self):
        self.trust = {}

    def update(self, entity_id: str, delta: float):
        current = self.trust.get(entity_id, 0.5)
        self.trust[entity_id] = max(0.0, min(1.0, current + delta))

    def get(self, entity_id: str) -> float:
        return self.trust.get(entity_id, 0.5)
