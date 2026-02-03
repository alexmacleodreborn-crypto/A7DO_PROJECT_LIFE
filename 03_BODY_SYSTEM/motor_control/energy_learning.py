class ActionEnergyLearner:
    """
    Learns to reduce energy cost for frequently attended actions.
    Learning is gated by BOTH attention and salience.
    """

    def __init__(
        self,
        decay: float = 0.05,
        floor: float = 0.3,
        min_salience: float = 0.2
    ):
        self.decay = decay
        self.floor = floor
        self.min_salience = min_salience
        self._cost_multiplier = {}  # action_name -> multiplier

    def learn(self, attended_memories):
        """
        Update efficiency based on attended memories.
        Only memories with sufficient salience cause learning.
        """
        for m in attended_memories:
            salience = m.get("salience", 0.0)
            if salience < self.min_salience:
                continue  # 🔒 NO LEARNING FROM NOISE

            event = m.get("event", {})
            if event.get("type") != "action":
                continue

            name = event.get("name")
            if not name:
                continue

            current = self._cost_multiplier.get(name, 1.0)
            improved = max(self.floor, current - self.decay)
            self._cost_multiplier[name] = improved

    def cost(self, action_name: str, base_cost: float) -> float:
        """
        Return adjusted energy cost for an action.
        """
        multiplier = self._cost_multiplier.get(action_name, 1.0)
        return base_cost * multiplier
