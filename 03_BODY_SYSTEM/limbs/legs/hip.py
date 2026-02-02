# limbs/legs/hip.py

from morphology.joints import Joint

class Hip(Joint):
    """
    Hip joint: locomotion anchor.
    """

    def __init__(self):
        super().__init__(min_angle=-120.0, max_angle=120.0)
