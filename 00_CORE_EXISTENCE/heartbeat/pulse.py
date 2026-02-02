# heartbeat/pulse.py

class Pulse:
    """
    Represents life pulse of A7DO.
    """

    ALIVE = "alive"
    PAUSED = "paused"
    DEGRADED = "degraded"
    DEAD = "dead"

    def __init__(self):
        self.state = self.ALIVE

    def set_state(self, state):
        self.state = state

    def is_alive(self):
        return self.state == self.ALIVE
