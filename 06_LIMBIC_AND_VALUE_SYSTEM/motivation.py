class MotivationState:
    """
    Represents longer-term motivational bias.
    Descriptive only.
    """

    def __init__(self):
        self.level = 0.0  # 0..1

    def set(self, value: float):
        self.level = max(0.0, min(1.0, value))

    def get(self) -> float:
        return self.level


class MotivationSystem:
    """
    Limbic motivation system.

    Reinforces salience for:
    - recurring action patterns
    - consistently attended memories
    - behaviors with sustained relevance

    Motivation is slow, stabilizing, and persistent.
    """

    def __init__(self, salience):
        """
        Parameters
        ----------
        salience : SalienceMap
            Central salience authority.
        """
        self.salience = salience
        self.state = MotivationState()

        # Track frequency of event types
        self._event_counts = {}

    def update(self, memory):
        """
        Update motivation-driven salience reinforcement.
        """
        recent = memory.recent(10)
        if not recent:
            return

        for m in recent:
            mem_id = m.get("id")
            if not mem_id:
                continue

            event = m.get("event", {})
            event_type = event.get("type")

            if not event_type:
                continue

            # Count occurrences
            self._event_counts[event_type] = (
                self._event_counts.get(event_type, 0) + 1
            )

            count = self._event_counts[event_type]

            # Slow reinforcement: grows with repetition
            if count >= 3:
                reinforcement = min(0.5, 0.1 * count)
                self.salience.set(mem_id, reinforcement)
                self.state.set(reinforcement)

    def current_level(self) -> float:
        """
        Return current motivation level.
        """
        return self.state.get()
