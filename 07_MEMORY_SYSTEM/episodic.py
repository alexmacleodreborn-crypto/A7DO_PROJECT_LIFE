from datetime import datetime, UTC

class EpisodicMemory:
    def __init__(self):
        self._events = []

    def record(self, event: dict):
        record = {
            "event": event,
            "time": datetime.now(UTC).isoformat()
        }
        self._events.append(record)
        return record

    def recent(self, n: int = 10):
        return self._events[-n:]
