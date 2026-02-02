# adolescent.py

class AdolescentStage:
    """
    Abstract thought and self-modeling.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": True,
            "motor": ["gross", "fine", "coordinated"],
            "memory": "all",
            "language": True,
            "metacognition": True
        }
