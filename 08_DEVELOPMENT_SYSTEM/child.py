# child.py

class ChildStage:
    """
    Fine motor and structured learning appear.
    """

    def allowed_systems(self):
        return {
            "heartbeat": True,
            "metabolism": True,
            "sensors": True,
            "motor": ["gross", "fine"],
            "memory": ["episodic", "procedural", "semantic"],
            "language": True
        }
