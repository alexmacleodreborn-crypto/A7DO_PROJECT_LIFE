# shutdown_authority.py

class ShutdownAuthority:
    """
    Ultimate shutdown controller.
    """

    def __init__(self):
        self.active = False

    def trigger(self, reason: str):
        self.active = True
        return {
            "shutdown": True,
            "reason": reason
        }

    def is_active(self) -> bool:
        return self.active
