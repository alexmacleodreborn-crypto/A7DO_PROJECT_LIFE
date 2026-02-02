# api.py

class A7DOAPI:
    """
    Read-only and request-based external interface.
    """

    def __init__(self, core_state: dict):
        self.core_state = core_state

    def status(self) -> dict:
        return {
            "identity": self.core_state.get("identity"),
            "lifecycle": self.core_state.get("lifecycle"),
            "energy": self.core_state.get("energy")
        }

    def request(self, request_type: str, payload: dict):
        """
        Requests must be routed through normal internal pipelines.
        This method does NOT execute actions.
        """
        return {
            "request_type": request_type,
            "payload": payload,
            "accepted": True
        }
