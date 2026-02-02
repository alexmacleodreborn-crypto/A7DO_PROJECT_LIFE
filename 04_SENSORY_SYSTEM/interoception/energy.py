# interoception/energy.py

class EnergySense:
    """
    Reports internal energy state.
    """

    def read(self, level):
        return {"energy_level": level}
