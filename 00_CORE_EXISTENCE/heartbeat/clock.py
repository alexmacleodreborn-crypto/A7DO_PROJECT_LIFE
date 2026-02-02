# heartbeat/clock.py

import time

class SystemClock:
    """
    Monotonic system clock.
    """

    def __init__(self):
        self.start_time = time.monotonic()

    def now(self):
        return time.monotonic() - self.start_time
