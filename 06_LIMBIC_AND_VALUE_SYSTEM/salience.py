# salience.py

class SalienceMap:
    """
    Central, authoritative salience store.

    Salience is an external value overlay on memory.
    Memory objects NEVER store salience directly.
    """

    def __init__(self):
        # memory_id -> salience value
        self._map: dict[str, float] = {}

    # ---------- Core API ----------

    def set(self, memory_id: str, value: float) -> None:
        """
        Register or update salience for a memory.
        """
        self._map[memory_id] = float(value)

    def get(self, memory_id: str) -> float:
        """
        Return current salience.
        Missing memory_ids return 0.0 (but are not registered).
        """
        return self._map.get(memory_id, 0.0)

    def has(self, memory_id: str) -> bool:
        """
        Return True if this memory has ever had salience assigned.
        """
        return memory_id in self._map

    def remove(self, memory_id: str) -> None:
        """
        Explicitly remove salience tracking for a memory.
        """
        self._map.pop(memory_id, None)

    def all(self) -> dict[str, float]:
        """
        Return a shallow copy of all salience values.
        """
        return dict(self._map)

    # ---------- Dynamics ----------

    def decay(self, rate: float) -> None:
        """
        Apply global decay to all salience values.
        Rate should be in (0, 1).
        """
        if not 0.0 <= rate <= 1.0:
            raise ValueError("Decay rate must be between 0 and 1")

        for k in self._map:
            self._map[k] *= (1.0 - rate)
