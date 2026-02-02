# agents.py

class WorldAgent:
    """
    Represents other agents in the world.
    """

    def __init__(self, agent_id: str):
        self.id = agent_id
        self.state = {}

    def act(self):
        return {"agent": self.id, "action": "idle"}
