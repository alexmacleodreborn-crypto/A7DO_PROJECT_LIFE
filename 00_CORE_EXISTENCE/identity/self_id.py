from datetime import datetime, UTC
import uuid

class SelfIdentity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(UTC).isoformat()
