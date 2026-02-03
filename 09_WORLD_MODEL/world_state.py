class WorldState:
    """
    Descriptive world model.
    Holds the current state of the organism and environment.
    NO learning, NO planning, NO decisions.
    """

    def __init__(self):
        self._state = {
            "energy": None,
            "strain": None,
            "last_action": None,
            "last_sensation": None,
            "time": None,
        }

    def update(self, **kwargs):
        """
        Update known world variables.
        Only overwrites provided keys.
        """
        for key, value in kwargs.items():
            if key in self._state:
                self._state[key] = value

    def snapshot(self):
        """
        Return a read-only snapshot of the current world state.
        """
        return dict(self._state)
