# toddler.py

class ToddlerStage:
    """
    Gross motor control emerges.
    Fine motor unreliable.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": True,
            "motor": "gross_only",
            "memory": ["episodic", "procedural"],
            "language": "symbols_only"
        }
