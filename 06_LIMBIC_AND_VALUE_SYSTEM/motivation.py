# motivation.py

class Motivation:
    """
    Internal drive intensity.
    """

    def __init__(self):
        self.level = 0.5  # baseline drive

    def increase(self, amount: float):
        self.level = min(1.0, self.level + amount)

    def decrease(self, amount: float):
        self.level = max(0.0, self.level - amount)

    def value(self) -> float:
        return self.level
