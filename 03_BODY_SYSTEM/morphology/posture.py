# morphology/posture.py

class Posture:
    """
    Tracks body stability.
    """

    def __init__(self):
        self.stable = True

    def destabilize(self):
        self.stable = False

    def stabilize(self):
        self.stable = True
