class Predictor:
    """
    Descriptive predictor.
    Uses world state and recent memory to forecast likely outcomes.
    NO learning, NO decisions.
    """

    def __init__(self, world_state, memory):
        self.world = world_state
        self.memory = memory

    def predict(self):
        snapshot = self.world.snapshot()
        recent = self.memory.recent(5)

        expected_strain = snapshot.get("strain", 0.0)
        confidence = 0.0

        # Simple heuristic: similar past events increase expectation
        for m in recent:
            event = m.get("event", {})
            if event.get("type") == "pain_withdrawal":
                past_strain = event.get("strain")
                if past_strain is not None:
                    expected_strain = max(expected_strain, past_strain)
                    confidence += 0.2

        confidence = min(confidence, 1.0)

        return {
            "expected_strain": expected_strain,
            "confidence": confidence,
        }
