class SalienceMap:
    def __init__(self):
        self._map = {}

    def set(self, memory_id: str, value: float):
        self._map[memory_id] = float(value)

    def get(self, memory_id: str) -> float:
        return self._map.get(memory_id, 0.0)
