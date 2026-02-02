# environment_sense/light.py

class LightSense:
    """
    Detects illumination.
    """

    def read(self, level):
        return {"light": level}
