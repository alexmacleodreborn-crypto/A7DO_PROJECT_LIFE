class WorldTime:
    """
    Tracks world time independently of A7DO.
    """
    def __init__(self):
        self.t = 0.0

    def tick(self, delta: float = 1.0):
        self.t += delta
        return self.t
