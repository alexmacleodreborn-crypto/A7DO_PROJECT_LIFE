# energy/fatigue.py

class Fatigue:
    """
    Accumulated strain from usage.
    """

    def __init__(self):
        self.level = 0.0

    def add(self, amount: float):
        self.level += amount

    def recover(self, amount: float):
        self.level = max(0.0, self.level - amount)
