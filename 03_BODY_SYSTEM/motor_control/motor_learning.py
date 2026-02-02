# motor_control/motor_learning.py

class MotorLearning:
    """
    Improves movement efficiency over time.
    """

    def __init__(self):
        self.skill = 0.0

    def practice(self):
        self.skill += 0.01
