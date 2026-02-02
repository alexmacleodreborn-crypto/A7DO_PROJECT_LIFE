# emotion_agent.py

class EmotionAgent:
    """
    Reports emotional context.
    """

    def assess(self, emotional_state: str) -> dict:
        return {
            "emotion": emotional_state,
            "intensity": 0.5
        }
