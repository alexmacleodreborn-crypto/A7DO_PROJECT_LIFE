# causality_graph.py

class CausalityGraph:
    """
    Tracks causal relationships in the world.
    """

    def __init__(self):
        self.edges = []

    def add(self, cause: str, effect: str):
        self.edges.append((cause, effect))

    def effects_of(self, cause: str):
        return [e for c, e in self.edges if c == cause]
