"""
A7DO Predictor
Forecasts future world state using history + present
with softened velocity scaling and controlled curvature.
"""

import math

class Predictor:
    def __init__(self, world, memory):
        self.world = world
        self.memory = memory

        # Curvature gain (kept modest)
        self.KAPPA = 0.15

    def predict(self, horizon: int = 2):
        """
        Predicts strain at t + horizon using:
        - softened velocity contribution
        - second-derivative curvature correction
        """

        # Current state
        current = self.world.snapshot()
        current_strain = current.get("strain", 0.0)

        # Recent memory
        recent = self.memory.recent(3)

        predicted = current_strain

        if len(recent) >= 2:
            try:
                s1 = recent[-1]["event"]["strain"]
                s0 = recent[-2]["event"]["strain"]

                # First derivative (velocity)
                velocity = s1 - s0

                # --- KEY CHANGE ---
                # Softened velocity scaling (nonlinear in horizon)
                velocity_scale = math.sqrt(horizon)

                predicted = current_strain + velocity_scale * velocity

                # Second derivative (curvature)
                if len(recent) >= 3:
                    s_1 = recent[-3]["event"]["strain"]
                    acceleration = s1 - 2 * s0 + s_1

                    predicted -= (
                        self.KAPPA * (horizon ** 2) * acceleration
                    )

            except Exception:
                predicted = current_strain

        # Clamp to physical bounds
        predicted = max(0.0, min(1.0, predicted))

        # Conservative base confidence (calibrated elsewhere)
        confidence = 0.2

        return {
            "expected_strain": predicted,
            "confidence": confidence,
            "horizon": horizon,
            "kappa": self.KAPPA,
            "velocity_scale": velocity_scale if len(recent) >= 2 else None,
        }
