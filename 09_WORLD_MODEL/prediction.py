class Predictor:
    """
    Read-only predictor.
    Observes world + memory, produces a forecast.
    """

    def __init__(self, horizon: int = 1, kappa: float = 0.15):
        self.horizon = horizon
        self.kappa = kappa
        self.last_prediction = None

    def predict(self, world_snapshot: dict, memory_recent: list):
        strain = world_snapshot.get("strain", 0.0)

        expected = max(0.0, min(1.0, strain + self.kappa))
        confidence = 0.2  # conservative by design

        self.last_prediction = {
            "expected_strain": expected,
            "confidence": confidence,
            "horizon": self.horizon,
            "kappa": self.kappa,
        }
        return self.last_prediction
