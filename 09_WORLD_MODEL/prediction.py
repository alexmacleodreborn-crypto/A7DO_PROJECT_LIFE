"""
A7DO Predictor
Forecasts future world state using history + present
with curvature (second-derivative) correction.
"""

class Predictor:
    def __init__(self, world, memory):
        self.world = world
        self.memory = memory

    def predict(self, horizon: int = 2):
        """
        Predicts strain at t + horizon using
        velocity + curvature correction.
        """

        # Current state
        current = self.world.snapshot()
        current_strain = current.get("strain", 0.0)

        # Get recent memory (need at least 3 points for curvature)
        recent = self.memory.recent(3)

        predicted = current_strain

        if len(recent) >= 2:
            try:
                s1 = recent[-1]["event"]["strain"]
                s0 = recent[-2]["event"]["strain"]
                velocity = s1 - s0

                predicted = current_strain + horizon * velocity

                # Curvature correction (second derivative)
                if len(recent) >= 3:
                    s_1 = recent[-3]["event"]["strain"]
                    acceleration = s1 - 2 * s0 + s_1

                    # Apply half-acceleration correction
                    predicted -= 0.5 * (horizon ** 2) * acceleration

            except Exception:
                predicted = current_strain

        # Clamp to valid range
        predicted = max(0.0, min(1.0, predicted))

        # Conservative base confidence (still calibrated elsewhere)
        confidence = 0.2

        return {
            "expected_strain": predicted,
            "confidence": confidence,
            "horizon": horizon,
        }
