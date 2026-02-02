# environments/society.py

class SocietyEnvironment:
    """
    Environment with many agents.
    """

    def __init__(self):
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)
