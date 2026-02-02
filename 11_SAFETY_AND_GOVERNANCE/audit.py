# audit.py

class AuditLog:
    """
    Records safety-relevant events.
    """

    def __init__(self):
        self.records = []

    def record(self, entry: dict):
        self.records.append(entry)

    def recent(self, n: int = 10):
        return self.records[-n:]
