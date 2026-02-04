from datetime import datetime, UTC
import uuid


class EpisodicMemory:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self._events = []

    def record(self, event: dict):
        record = {
            "id": str(uuid.uuid4()),
            "event": event,
            "time": datetime.now(UTC).isoformat(),
        }
        self._events.append(record)
        self._prune_if_needed()
        return record

    def tick(self):
        # Memory itself does NOT decay value.
        # Salience decay happens in SalienceMap.
        pass

    def _prune_if_needed(self):
        if len(self._events) <= self.capacity:
            return

        # Prune oldest memories only (FIFO)
        while len(self._events) > self.capacity:
            self._events.pop(0)

    def recent(self, n: int = 10):
        return self._events[-n:]
