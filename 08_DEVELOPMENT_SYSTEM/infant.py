# infant.py

class InfantStage:
    """
    Sensory input allowed.
    Motor output is reflex-only.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": True,
            "motor": "reflex_only",
            "memory": "episodic_only",
            "language": False
        }
