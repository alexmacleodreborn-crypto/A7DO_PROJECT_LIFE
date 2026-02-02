# interoception/comfort.py

class ComfortSense:
    """
    Reports comfort/discomfort.
    """

    def read(self, level):
        return {"comfort": level}
