class AttentionSystem:
    """
    Read-only attention mechanism.
    Selects top-N memories by salience.
    """

    def __init__(self, memory, focus_size=3):
        self.memory = memory
        self.focus_size = focus_size

    def focus(self):
        # Read-only: do NOT mutate memory
        ordered = sorted(
            self.memory.recent(100),
            key=lambda m: m.get("salience", 0.0),
            reverse=True
        )
        return ordered[: self.focus_size]
