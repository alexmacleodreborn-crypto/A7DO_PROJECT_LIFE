# energy/metabolism.py

class Metabolism:
    """
    Interface between actions and UnifiedEnergy.

    Converts discrete actions into immediate energy costs.
    Does NOT handle recovery or time-based flow.
    """

    def __init__(self, unified_energy):
        self.energy = unified_energy

    def spend(self, cost: float):
        """
        Spend energy for an action.
        Physics enforcement is delegated to UnifiedEnergy.
        """
        self.energy.consume(cost)
