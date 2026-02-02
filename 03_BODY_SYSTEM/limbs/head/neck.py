# limbs/head/neck.py

from morphology.joints import Joint

class Neck(Joint):
    """
    Neck joint: head support.
    """

    def __init__(self):
        super().__init__(min_angle=-90.0, max_angle=90.0)
