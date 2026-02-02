# curvature/spacetime.py

class Spacetime:
    """
    Enforces locality and continuity.
    """

    def propagate(self, value: float, distance: float) -> float:
        if distance <= 0:
            return value
        return value / (1.0 + distance)
