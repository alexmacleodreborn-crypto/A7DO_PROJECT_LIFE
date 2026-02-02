# scalar_field/visibility.py

class ScalarVisibility:
    """
    Limits what can be sensed or inferred.
    """

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold

    def is_visible(self, magnitude: float) -> bool:
        return abs(magnitude) >= self.threshold
