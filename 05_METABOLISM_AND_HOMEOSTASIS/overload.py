# overload.py

class OverloadMonitor:
    """
    Detects excessive demand on the system.
    """

    def __init__(self):
        self.strain = 0.0

    def apply_load(self, amount: float):
        self.strain += amount
        if self.strain > 1.0:
            raise RuntimeError("System overload")

    def recover(self, amount: float):
        self.strain = max(0.0, self.strain - amount)
