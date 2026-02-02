# environment_sense/atmosphere.py

class AtmosphereSense:
    """
    Detects atmospheric conditions.
    """

    def read(self, composition):
        return {"atmosphere": composition}
