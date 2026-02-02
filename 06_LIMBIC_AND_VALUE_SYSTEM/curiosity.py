# curiosity.py

class Curiosity:
    """
    Preference for novelty.
    """

    def __init__(self):
        self.novelty_bias = 0.5

    def update(self, novelty: float):
        # novelty ∈ [0,1]
        self.novelty_bias = (self.novelty_bias + novelty) / 2

    def value(self) -> float:
        return self.novelty_bias
