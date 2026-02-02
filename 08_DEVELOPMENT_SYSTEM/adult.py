# adult.py

class AdultStage:
    """
    Full system access under physics and ethics.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": True,
            "motor": "all",
            "memory": "all",
            "language": True,
            "metacognition": True,
            "planning": True
        }
