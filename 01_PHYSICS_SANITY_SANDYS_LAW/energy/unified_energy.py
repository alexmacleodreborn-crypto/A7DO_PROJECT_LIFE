# energy/unified_energy.py

class UnifiedEnergy:
    """
    Tracks total available energy.
    """

    def __init__(self, total: float):
        self.total = total

    def consume(self, amount: float):
        if amount > self.total:
            raise RuntimeError("Energy budget exceeded")
        self.total -= amount
