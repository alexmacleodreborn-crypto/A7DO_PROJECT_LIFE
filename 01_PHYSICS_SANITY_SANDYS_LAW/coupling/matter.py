# coupling/matter.py

class MatterCoupling:
    """
    Resistance from physical structure.
    """

    def resist(self, effort: float, mass: float) -> float:
        if mass <= 0:
            raise ValueError("Mass must be positive")
        return effort / mass
