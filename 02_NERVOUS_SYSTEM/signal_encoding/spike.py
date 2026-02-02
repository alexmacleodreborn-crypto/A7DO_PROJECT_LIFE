# signal_encoding/spike.py

class SpikeSignal:
    """
    Binary or graded spike representation.
    """

    def __init__(self, magnitude: float):
        self.magnitude = magnitude
