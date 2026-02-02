# coupling/gravity.py

class GravityCoupling:
    """
    Simple attraction constraint.
    """

    def attract(self, value: float, well: float) -> float:
        return value * (1.0 / (1.0 + well))
