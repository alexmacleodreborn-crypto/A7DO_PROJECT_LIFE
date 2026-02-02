# semantic.py

class SemanticMemory:
    """
    Stores factual knowledge.
    """

    def __init__(self):
        self.knowledge = {}

    def store(self, key: str, value):
        self.knowledge[key] = value

    def retrieve(self, key: str):
        return self.knowledge.get(key)
