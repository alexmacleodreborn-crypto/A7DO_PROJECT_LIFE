# proprioception/balance.py

class BalanceSense:
    """
    Detects stability.
    """

    def check(self, stable: bool):
        return {"balanced": stable}
