from datetime import datetime, UTC

class EpisodicMemory:
    def __init__(self, capacity=100, decay_rate=0.01):
        self.capacity = capacity
        self.decay_rate = decay_rate
        self._events = []

    def record(self, event: dict, salience: float = 0.0):
        record = {
            "event": event,
            "time": datetime.now(UTC).isoformat(),
            "salience": salience,
        }
        self._events.append(record)
        self._prune_if_needed()
        return record

    def tick(self):
        # Salience decay
        for m in self._events:
            m["salience"] = max(0.0, m["salience"] - self.decay_rate)
        self._prune_if_needed()

    def _prune_if_needed(self):
        if len(self._events) <= self.capacity:
            return

        # Sort by salience ascending (lowest first)
        self._events.sort(key=lambda m: m["salience"])
        while len(self._events) > self.capacity:
            self._events.pop(0)

    def recent(self, n: int = 10):
        return self._events[-n:]
