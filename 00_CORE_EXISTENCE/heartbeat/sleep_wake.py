# heartbeat/sleep_wake.py

class SleepWakeCycle:
    """
    Explicit sleep / wake state.

    This class holds state ONLY.
    Decisions about when to sleep/wake are made by LifeLoop.
    """

    def __init__(self):
        self.awake = True

    def sleep(self):
        self.awake = False

    def wake(self):
        self.awake = True

    def state(self) -> str:
        return "awake" if self.awake else "asleep"
