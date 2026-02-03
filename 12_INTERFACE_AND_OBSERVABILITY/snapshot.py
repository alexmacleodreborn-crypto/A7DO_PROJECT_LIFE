class IntrospectionSnapshot:
    """
    Read-only introspection snapshot.
    Captures current internal state for visualization or debugging.
    """

    def __init__(self, world, memory, attention, predictor, council):
        self.world = world
        self.memory = memory
        self.attention = attention
        self.predictor = predictor
        self.council = council

    def capture(self):
        return {
            "world": self.world.snapshot(),
            "memory": [
                m.get("event") for m in self.memory.recent(10)
            ],
            "attention": [
                m.get("event") for m in self.attention.focus()
            ],
            "prediction": self.predictor.predict(),
            "council": self.council.deliberate(),
        }
