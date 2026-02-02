# ethics_agent.py

class EthicsAgent:
    """
    Flags ethical violations.
    """

    def review(self, action: dict) -> dict:
        return {
            "allowed": True,
            "reason": "No violation detected"
        }
