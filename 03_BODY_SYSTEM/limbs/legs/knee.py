# limbs/legs/knee.py

from morphology.joints import Joint

class Knee(Joint):
    """
    Knee joint: walking support.
    """

    def __init__(self):
        super().__init__(min_angle=0.0, max_angle=150.0)
