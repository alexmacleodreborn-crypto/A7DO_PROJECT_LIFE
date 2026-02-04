class Persona:
    """
    Defines the current personality or behavioral mode of A7DO.
    """

    def __init__(self, name="core", traits=None):
        self.name = name
        self.traits = traits or []

    def describe(self):
        return {
            "persona": self.name,
            "traits": self.traits
        }

    def has_trait(self, trait):
        return trait in self.traits
