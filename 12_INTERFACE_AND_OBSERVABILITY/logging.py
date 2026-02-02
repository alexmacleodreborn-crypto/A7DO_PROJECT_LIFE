# logging.py

from datetime import datetime

class EventLogger:
    """
    Records observable system events.
    """

    def __init__(self):
        self.events = []

    def log(self, category: str, message: str):
        self.events.append({
            "time": datetime.utcnow().isoformat(),
            "category": category,
            "message": message
        })

    def recent(self, n: int = 20):
        return self.events[-n:]
