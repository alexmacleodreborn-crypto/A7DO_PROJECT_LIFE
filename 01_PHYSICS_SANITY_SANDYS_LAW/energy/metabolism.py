# energy/metabolism.py

class Metabolism:
    """
    Converts energy into action.
    """

    def __init__(self, energy_system):
        self.energy = energy_system

    def spend(self, cost: float):
        self.energy.consume(cost)
