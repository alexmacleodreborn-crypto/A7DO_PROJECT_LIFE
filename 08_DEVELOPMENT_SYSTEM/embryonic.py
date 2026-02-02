# embryonic.py

class EmbryonicStage:
    """
    No awareness. No control. No memory.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": False,
            "motor": False,
            "memory": False,
            "language": False
        }
