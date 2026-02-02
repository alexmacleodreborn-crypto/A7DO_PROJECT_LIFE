# touch/pressure.py

class PressureSensor:
    """
    Detects contact force.
    """

    def read(self, force):
        return {"pressure": force}
