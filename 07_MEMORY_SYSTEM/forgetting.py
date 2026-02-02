# forgetting.py

class ForgettingMechanism:
    """
    Removes or weakens old memories.
    """

    def decay(self, memories: list, keep_last: int = 100):
        if len(memories) <= keep_last:
            return memories
        return memories[-keep_last:]
