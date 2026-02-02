# conservation.py

class ConservationLaw:
    """
    Enforces conservation of energy and effort.
    """

    def check(self, cost: float, available: float):
        if cost > available:
            raise RuntimeError("Conservation violation: insufficient energy")
