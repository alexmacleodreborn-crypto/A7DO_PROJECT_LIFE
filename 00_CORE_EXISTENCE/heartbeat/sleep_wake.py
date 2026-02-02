# heartbeat/sleep_wake.py

class SleepWakeCycle:
    """
    Manages rest vs activity states.
    """

    def __init__(self):
        self.awake = True

    def sleep(self):
        self.awake = False

    def wake(self):
        self.awake = True
