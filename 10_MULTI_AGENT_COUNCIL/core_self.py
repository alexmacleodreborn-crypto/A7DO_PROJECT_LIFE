# core_self.py

class CoreSelf:
    """
    Maintains identity coherence.
    """

    def __init__(self, self_id: str):
        self.self_id = self_id

    def identity(self) -> str:
        return self.self_id
