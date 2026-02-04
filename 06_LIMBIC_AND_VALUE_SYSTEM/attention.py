class AttentionSystem:
    """
    Read-only attention mechanism.
    Selects top-N memories by external salience.
    """

    def __init__(self, memory, salience, focus_size=3):
        self.memory = memory
        self.salience = salience
        self.focus_size = focus_size

    def focus(self):
        recent = self.memory.recent(100)

        ordered = sorted(
            recent,
            key=lambda m: self.salience.get(m["id"]),
            reverse=True
        )

        return ordered[: self.focus_size]

