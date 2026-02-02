# critic_agent.py

class CriticAgent:
    """
    Highlights risks and weaknesses.
    """

    def critique(self, plan: dict) -> dict:
        return {
            "plan": plan,
            "risks": []
        }
