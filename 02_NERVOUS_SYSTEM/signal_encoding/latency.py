# signal_encoding/latency.py

import time

class Latency:
    """
    Adds transmission delay.
    """

    def apply(self, delay_ms: int):
        time.sleep(delay_ms / 1000.0)
