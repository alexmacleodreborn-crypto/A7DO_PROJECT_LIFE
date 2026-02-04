class EmotionalState:
    """
    Represents current affective balance.
    Descriptive only — does not cause action directly.
    """

    def __init__(self):
        self.state = "neutral"

    def set(self, state: str):
        self.state = state

    def get(self) -> str:
        return self.state


class EmotionSystem:
    """
    Limbic emotion system.

    Reads recent memory and writes salience.
    May update internal emotional state.
    """

    def __init__(self, salience):
        """
        Parameters
        ----------
        salience : SalienceMap
            Central salience authority.
        """
        self.salience = salience
        self.state = EmotionalState()

    def update(self, memory):
        """
        Update emotional state and salience based on recent memory.
        """
        recent = memory.recent(5)
        if not recent:
            return

        for m in recent:
            mem_id = m.get("id")
            if not mem_id:
                continue

            event = m.get("event", {})
            event_type = event.get("type")

            # Simple example emotion logic
            if event_type == "action":
                # Actions are mildly salient
                self.salience.set(mem_id, 0.3)
                self.state.set("engaged")

            elif event_type == "pain":
                # Pain spikes salience strongly
                self.salience.set(mem_id, 0.8)
                self.state.set("distressed")

            else:
                # Unknown events get low salience
                self.salience.set(mem_id, 0.1)

    def current_state(self) -> str:
        """
        Return current emotional label.
        """
        return self.state.get()
