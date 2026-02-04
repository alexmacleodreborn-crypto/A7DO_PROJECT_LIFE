class ActionEnergyLearner:
    def __init__(self, salience, decay=0.05, floor=0.3, min_salience=0.2):
        self.salience = salience
        self.decay = decay
        self.floor = floor
        self.min_salience = min_salience
        self._cost_multiplier = {}

    def learn(self, attended_memories):
        for m in attended_memories:
            mem_id = m["id"]
            sal = self.salience.get(mem_id)

            if sal < self.min_salience:
                continue

            event = m.get("event", {})
            if event.get("type") != "action":
                continue

            name = event.get("name")
            if not name:
                continue

            current = self._cost_multiplier.get(name, 1.0)
            self._cost_multiplier[name] = max(
                self.floor, current - self.decay
            )
