# limbs/arms/elbow.py

from morphology.joints import Joint

class Elbow(Joint):
    """
    Elbow joint: flexion/extension.
    """

    def __init__(self):
        super().__init__(min_angle=0.0, max_angle=145.0)
