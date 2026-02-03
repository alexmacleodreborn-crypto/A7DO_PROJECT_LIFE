"""
A7DO Predictor
Forecasts future world state using history + present.
"""

class Predictor:
    def __init__(self, world, memory):
        self.world = world
        self.memory = memory

    def predict(self, horizon: int = 2):
        """
        Predicts strain at t + horizon using recent trend.
        """

        # Current state
        current = self.world.snapshot()
        current_strain = current.get("strain", 0.0)

        # Get recent memory
        recent = self.memory.recent(2)

        # Default: no trend
        predicted = current_strain

        # If we have at least two past points, estimate trend
        if len(recent) >= 2:
            try:
                s1 = recent[-1]["event"]["strain"]
                s0 = recent[-2]["event"]["strain"]
                delta = s1 - s0

                # Simple linear extrapolation
                predicted = current_strain + horizon * delta
            except Exception:
                predicted = current_strain

        # Clamp to valid range
        predicted = max(0.0, min(1.0, predicted))

        # Conservative base confidence (still calibrated later)
        confidence = 0.2

        return {
            "expected_strain": predicted,
            "confidence": confidence,
            "horizon": horizon,
        }

