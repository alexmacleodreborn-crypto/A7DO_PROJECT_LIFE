# olfaction/smell.py

class SmellSensor:
    """
    Detects airborne chemicals.
    """

    def detect(self, compounds):
        return {"smell_vector": compounds}
