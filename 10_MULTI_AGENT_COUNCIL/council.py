class Council:
    """
    Read-only deliberative council.
    Aggregates multiple perspectives over the same state.
    NO action authority.
    """

    def __init__(self, world, memory, predictor, attention):
        self.world = world
        self.memory = memory
        self.predictor = predictor
        self.attention = attention

    def deliberate(self):
        snapshot = self.world.snapshot()
        focus = self.attention.focus()
        forecast = self.predictor.predict()

        opinions = {}

        # Voice 1: Risk assessor
        opinions["risk_assessor"] = {
            "current_strain": snapshot.get("strain"),
            "expected_strain": forecast.get("expected_strain"),
            "confidence": forecast.get("confidence"),
        }

        # Voice 2: Memory observer
        opinions["memory_observer"] = {
            "recent_events": [
                m.get("event", {}).get("type")
                for m in focus
            ]
        }

        # Voice 3: Prediction reader
        opinions["prediction_reader"] = {
            "forecast": forecast
        }

        return opinions
