# vision/motion.py

class MotionDetection:
    """
    Detects movement in visual field.
    """

    def detect(self, previous, current):
        return {"motion": previous != current}
