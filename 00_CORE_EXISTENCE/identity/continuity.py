# identity/continuity.py

class ContinuityGuard:
    """
    Ensures identity and memory continuity across cycles.
    """

    def __init__(self, identity):
        self.identity = identity
        self.last_tick = None

    def validate(self, current_tick):
        if self.last_tick is not None and current_tick <= self.last_tick:
            raise RuntimeError("Continuity violation: time reversal detected")
        self.last_tick = current_tick
