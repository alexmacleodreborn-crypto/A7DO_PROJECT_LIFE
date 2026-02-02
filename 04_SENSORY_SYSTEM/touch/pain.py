# touch/pain.py

class PainSensor:
    """
    Signals potential damage.
    """

    def trigger(self, level):
        return {"pain": level}
