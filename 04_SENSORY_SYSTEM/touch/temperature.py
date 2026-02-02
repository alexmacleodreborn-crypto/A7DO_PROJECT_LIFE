# touch/temperature.py

class TemperatureSensor:
    """
    Detects temperature.
    """

    def read(self, temp):
        return {"temperature": temp}
