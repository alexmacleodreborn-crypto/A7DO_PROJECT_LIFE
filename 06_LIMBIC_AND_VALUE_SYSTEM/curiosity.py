class CuriosityState:
    """
    Represents exploratory drive level.
    Descriptive only.
    """

    def __init__(self):
        self.level = 0.0  # 0..1

    def set(self, value: float):
        self.level = max(0.0, min(1.0, value))

    def get(self) -> float:
        return self.level


class CuriositySystem:
    """
    Limbic curiosity system.

    Increases salience for:
    - novel events
    - rarely seen event types
    - unexplored situations

    Does NOT cause action directly.
    """

    def __init__(self, salience):
        """
        Parameters
        ----------
        salience : SalienceMap
            Central salience authority.
        """
        self.salience = salience
        self.state = CuriosityState()
        self._seen_event_types = set()

    def update(self, memory):
        """
        Update curiosity-driven salience based on novelty.
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

            if not event_type:
                continue

            # Novel event type → curiosity spike
            if event_type not in self._seen_event_types:
                self.salience.set(mem_id, 0.6)
                self.state.set(0.6)
                self._seen_event_types.add(event_type)
            else:
                # Familiar events get mild curiosity
                self.salience.set(mem_id, 0.2)
                self.state.set(0.2)

    def current_level(self) -> float:
        """
        Return current curiosity level.
        """
        return self.state.get()
