"""
A7DO Predictor
Forecasts future world state using history + present
with controlled curvature (second-derivative) correction.
"""

class Predictor:
    def __init__(self, world, memory):
        self.world = world
        self.memory = memory

        # Curvature gain (stability parameter)
        # 0.0 = first-order only
        # ~0.15–0.3 = stable second-order correction
        self.KAPPA = 0.15

    def predict(self, horizon: int = 2):
        """
        Predicts strain at t + horizon using
        velocity + controlled curvature correction.
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

                # First derivative (velocity)
                velocity = s1 - s0
                predicted = current_strain + horizon * velocity

                # Second derivative (curvature / acceleration)
                if len(recent) >= 3:
                    s_1 = recent[-3]["event"]["strain"]
                    acceleration = s1 - 2 * s0 + s_1

                    # Controlled curvature correction
                    predicted -= (
                        self.KAPPA * (horizon ** 2) * acceleration
                    )

            except Exception:
                predicted = current_strain

        # Clamp to valid physical range
        predicted = max(0.0, min(1.0, predicted))

        # Conservative base confidence (calibrated elsewhere)
        confidence = 0.2

        return {
            "expected_strain": predicted,
            "confidence": confidence,
            "horizon": horizon,
            "kappa": self.KAPPA,
        }
