# interoception/stress.py

class StressSense:
    """
    Reports stress level.
    """

    def read(self, level):
        return {"stress": level}
