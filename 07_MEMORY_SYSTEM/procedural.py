# procedural.py

class ProceduralMemory:
    """
    Stores learned procedures and skills.
    """

    def __init__(self):
        self.skills = {}

    def learn(self, skill: str, proficiency: float):
        self.skills[skill] = max(0.0, min(1.0, proficiency))

    def get(self, skill: str):
        return self.skills.get(skill, 0.0)
