# morphology/skeleton.py

class Skeleton:
    """
    Defines hard structural constraints.
    """

    def __init__(self):
        self.integrity = 1.0  # 1.0 = intact

    def damage(self, amount: float):
        self.integrity = max(0.0, self.integrity - amount)
