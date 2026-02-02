# trait_scoring.py

class TraitScoring:
    """
    Aggregates evidence into trait-level scores.
    """

    def __init__(self):
        self.traits = {}

    def update(self, trait: str, value: float):
        current = self.traits.get(trait, 0.0)
        self.traits[trait] = (current + value) / 2

    def score(self, trait: str) -> float:
        return self.traits.get(trait, 0.0)

    def all(self):
        return dict(self.traits)
