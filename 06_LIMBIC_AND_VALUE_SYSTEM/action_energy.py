class ActionEnergyLearner:
    """
    Learns to reduce energy cost for frequently attended actions.

    Learning is gated by:
    - attention (only focused memories are considered)
    - salience (only meaningful events cause learning)

    This class NEVER mutates memory or energy directly.
    It only learns cost multipliers.
    """

    def __init__(
        self,
        salience,
        decay: float = 0.05,
        floor: float = 0.3,
        min_salience: float = 0.2,
    ):
        """
        Parameters
        ----------
        salience : SalienceMap
            Central salience authority.
        decay : float
            Learning rate per attended event.
        floor : float
            Minimum multiplier (hard efficiency limit).
        min_salience : float
            Salience threshold required for learning.
        """
        self.salience = salience
        self.decay = decay
        self.floor = floor
        self.min_salience = min_salience

        # action_name -> cost multiplier
        self._cost_multiplier = {}

    # --------------------------------------------------
    # LEARNING
    # --------------------------------------------------
    def learn(self, attended_memories):
        """
        Update efficiency based on attended memories.
        """
        for m in attended_memories:
            mem_id = m.get("id")
            if not mem_id:
                continue

            sal = self.salience.get(mem_id)
            if sal < self.min_salience:
                continue  # 🔒 No learning from low-importance events

            event = m.get("event", {})
            if event.get("type") != "action":
                continue

            action_name = event.get("name")
            if not action_name:
                continue

            current = self._cost_multiplier.get(action_name, 1.0)
            improved = max(self.floor, current - self.decay)

            self._cost_multiplier[action_name] = improved

    # --------------------------------------------------
    # QUERY
    # --------------------------------------------------
    def cost(self, action_name: str, base_cost: float) -> float:
        """
        Return adjusted energy cost for an action.
        """
        multiplier = self._cost_multiplier.get(action_name, 1.0)
        return base_cost * multiplier

    # --------------------------------------------------
    # DEBUG / INSPECTION
    # --------------------------------------------------
    def snapshot(self) -> dict:
        """
        Return current learned multipliers (for dashboards/tests).
        """
        return dict(self._cost_multiplier)
