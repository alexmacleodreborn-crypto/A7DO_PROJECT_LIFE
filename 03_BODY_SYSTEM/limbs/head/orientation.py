# limbs/head/orientation.py

class HeadOrientation:
    """
    Tracks head direction in space.
    """

    def __init__(self):
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0

    def update(self, yaw: float, pitch: float, roll: float):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
