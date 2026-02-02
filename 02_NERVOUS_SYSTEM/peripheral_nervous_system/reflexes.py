# peripheral_nervous_system/reflexes.py

class ReflexArc:
    """
    Immediate response without reasoning.
    """

    def respond(self, stimulus):
        return {"reflex": stimulus}
