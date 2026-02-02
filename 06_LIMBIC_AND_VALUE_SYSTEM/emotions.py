# emotions.py

class EmotionalState:
    """
    Represents current affective balance.
    Does not cause action directly.
    """

    def __init__(self):
        self.state = "neutral"

    def set(self, state: str):
        self.state = state

    def get(self) -> str:
        return self.state
