# central_nervous_system/consciousness.py

class Consciousness:
    """
    Represents moment-to-moment awareness.
    No memory, no reasoning here.
    """

    def __init__(self):
        self.active = True

    def is_active(self) -> bool:
        return self.active
