# limbs/legs/ankle.py

from morphology.joints import Joint

class Ankle(Joint):
    """
    Ankle joint: balance control.
    """

    def __init__(self):
        super().__init__(min_angle=-45.0, max_angle=45.0)
