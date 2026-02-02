# limbs/arms/wrist.py

from morphology.joints import Joint

class Wrist(Joint):
    """
    Wrist joint: fine orientation control.
    """

    def __init__(self):
        super().__init__(min_angle=-90.0, max_angle=90.0)
