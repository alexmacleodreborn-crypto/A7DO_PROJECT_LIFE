# energy_budget.py

class EnergyBudget:
    """
    Tracks available metabolic energy.
    All cognition and motion draw from here.
    """

    def __init__(self, capacity: float):
        self.capacity = capacity
        self.available = capacity

    def spend(self, amount: float):
        if amount > self.available:
            raise RuntimeError("Energy depleted")
        self.available -= amount

    def replenish(self, amount: float):
        self.available = min(self.capacity, self.available + amount)

    def level(self) -> float:
        return self.available
