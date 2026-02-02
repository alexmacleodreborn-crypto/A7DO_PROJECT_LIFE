# morphology/joints.py

class Joint:
    """
    Joint with angular limits.
    """

    def __init__(self, min_angle: float, max_angle: float):
        self.min = min_angle
        self.max = max_angle
        self.angle = 0.0

    def move(self, delta: float):
        new_angle = self.angle + delta
        if new_angle < self.min or new_angle > self.max:
            raise RuntimeError("Joint limit exceeded")
        self.angle = new_angle
